#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.infrastructure.database import SessionLocal, create_tables
from app.domain.models import (
    User, UserType, 
    Community, CommunityType, CommunityMembership, MembershipRole,
    Event, EventType, EventRegistration,
    Post, PostStatus, Comment
)

def init_users(db: Session):
    print("Creating users...")
    
    users_data = [
        {
            "name": "Ana Silva Santos",
            "email": "ana.silva@sicoob.com.br", 
            "phone": "(11) 98765-4321",
            "user_type": UserType.ENTREPRENEUR
        },
        {
            "name": "Carlos Eduardo Oliveira",
            "email": "carlos.oliveira@sicoob.com.br",
            "phone": "(11) 97654-3210", 
            "user_type": UserType.YOUNG
        },
        {
            "name": "Maria José Costa",
            "email": "maria.costa@sicoob.com.br",
            "phone": "(11) 96543-2109",
            "user_type": UserType.RETIREE
        },
        {
            "name": "João Paulo Ferreira",
            "email": "joao.ferreira@sicoob.com.br",
            "phone": "(11) 95432-1098",
            "user_type": UserType.GENERAL
        },
        {
            "name": "Patricia Souza Lima",
            "email": "patricia.lima@sicoob.com.br",
            "phone": "(11) 94321-0987",
            "user_type": UserType.ENTREPRENEUR
        },
        {
            "name": "Roberto da Silva Neto",
            "email": "roberto.neto@sicoob.com.br",
            "phone": "(11) 93210-9876",
            "user_type": UserType.GENERAL
        },
        {
            "name": "Fernanda Alves Pereira",
            "email": "fernanda.alves@sicoob.com.br",
            "phone": "(11) 92109-8765",
            "user_type": UserType.YOUNG
        },
        {
            "name": "Antônio Carlos Mendes",
            "email": "antonio.mendes@sicoob.com.br",
            "phone": "(11) 91098-7654",
            "user_type": UserType.RETIREE
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)
    
    db.commit()
    
    for user in users:
        db.refresh(user)
    
    print(f"{len(users)} users created!")
    return users

def init_communities(db: Session, users):
    print("Creating communities...")
    
    communities_data = [
        {
            "name": "Jovens Empreendedores",
            "description": "Comunidade para jovens cooperados compartilharem experiências de empreendedorismo e inovação.",
            "community_type": CommunityType.PUBLIC,
            "max_members": 100,
            "owner_id": users[1].id,  # Carlos (jovem)
            "rules": "1. Seja respeitoso\n2. Compartilhe conhecimento\n3. Ajude outros jovens empreendedores"
        },
        {
            "name": "Experiência e Sabedoria",
            "description": "Espaço para cooperados com mais experiência compartilharem conhecimentos e mentorias.",
            "community_type": CommunityType.PUBLIC,
            "max_members": 50,
            "owner_id": users[2].id,  # Maria José (aposentada)
            "rules": "1. Compartilhe experiências\n2. Seja mentor\n3. Pratique a cooperação"
        },
        {
            "name": "Negócios e Oportunidades",
            "description": "Comunidade privada para discussão de oportunidades de negócios entre empreendedores da cooperativa.",
            "community_type": CommunityType.PRIVATE,
            "max_members": 30,
            "owner_id": users[0].id,  # Ana Silva (empreendedora)
            "rules": "1. Confidencialidade das informações\n2. Parcerias éticas\n3. Transparência nos negócios"
        },
        {
            "name": "Capacitação Financeira",
            "description": "Grupo para educação financeira e discussão sobre investimentos e economia.",
            "community_type": CommunityType.PUBLIC,
            "max_members": 200,
            "owner_id": users[3].id,  # João Paulo
            "rules": "1. Informações baseadas em fatos\n2. Não aconselhamento financeiro pessoal\n3. Educação em primeiro lugar"
        }
    ]
    
    communities = []
    for comm_data in communities_data:
        community = Community(**comm_data)
        db.add(community)
        communities.append(community)
    
    db.commit()
    
    for community in communities:
        db.refresh(community)
    
    print(f"{len(communities)} communities created!")
    return communities

def init_memberships(db: Session, users, communities):
    print("Creating memberships...")
    
    memberships_count = 0
    
    # Add owners as members with OWNER role
    for community in communities:
        membership = CommunityMembership(
            community_id=community.id,
            user_id=community.owner_id,
            role=MembershipRole.OWNER
        )
        db.add(membership)
        memberships_count += 1
    
    # Add other members to public communities
    public_communities = [c for c in communities if c.community_type == CommunityType.PUBLIC]
    
    # Young Entrepreneurs - add young and entrepreneur types
    young_entrepre_comm = next(c for c in communities if "Jovens" in c.name)
    for user in users:
        if user.user_type in [UserType.YOUNG, UserType.ENTREPRENEUR] and user.id != young_entrepre_comm.owner_id:
            membership = CommunityMembership(
                community_id=young_entrepre_comm.id,
                user_id=user.id,
                role=MembershipRole.MEMBER if user.user_type == UserType.YOUNG else MembershipRole.MODERATOR
            )
            db.add(membership)
            memberships_count += 1
    
    # Experience and Wisdom - add retirees and some general types
    exp_comm = next(c for c in communities if "Experiência" in c.name)
    for user in users:
        if user.user_type in [UserType.RETIREE, UserType.GENERAL] and user.id != exp_comm.owner_id:
            membership = CommunityMembership(
                community_id=exp_comm.id,
                user_id=user.id,
                role=MembershipRole.MEMBER
            )
            db.add(membership)
            memberships_count += 1
    
    # Financial Education - add all types
    cap_comm = next(c for c in communities if "Capacitação" in c.name)
    for user in users[:6]:  # Add first 6 users
        if user.id != cap_comm.owner_id:
            membership = CommunityMembership(
                community_id=cap_comm.id,
                user_id=user.id,
                role=MembershipRole.MEMBER
            )
            db.add(membership)
            memberships_count += 1
    
    db.commit()
    
    # Update member counts
    for community in communities:
        member_count = db.query(CommunityMembership).filter(
            CommunityMembership.community_id == community.id,
            CommunityMembership.active == True
        ).count()
        community.member_count = member_count
    
    db.commit()
    
    print(f"{memberships_count} memberships created!")

def init_events(db: Session, users):
    print("Creating events...")
    
    now = datetime.now()
    
    events_data = [
        {
            "title": "Feira de Cooperativismo 2025",
            "description": "Grande feira anual de cooperativismo com exposições, palestras e networking entre cooperados.",
            "event_type": EventType.COOPERATIVE_FAIR,
            "start_date": now + timedelta(days=30),
            "end_date": now + timedelta(days=32),
            "location": "Centro de Convenções Sicoob",
            "address": "Av. das Cooperativas, 1000 - Centro",
            "max_capacity": 500,
            "organizer_id": users[0].id
        },
        {
            "title": "Palestra: Educação Financeira para Jovens",
            "description": "Palestra especial sobre planejamento financeiro e investimentos para jovens cooperados.",
            "event_type": EventType.LECTURE,
            "start_date": now + timedelta(days=15),
            "end_date": now + timedelta(days=15, hours=2),
            "location": "Auditório Principal Sicoob",
            "address": "Rua da Cooperação, 500 - Centro",
            "max_capacity": 100,
            "organizer_id": users[1].id
        },
        {
            "title": "Rodada de Negócios - Agronegócio",
            "description": "Encontro entre cooperados do agronegócio para discussão de parcerias e oportunidades de negócios.",
            "event_type": EventType.BUSINESS_ROUND,
            "start_date": now + timedelta(days=45),
            "end_date": now + timedelta(days=45, hours=4),
            "location": "Sala de Reuniões Executiva",
            "address": "Rua da Cooperação, 500 - Sala 201",
            "max_capacity": 25,
            "organizer_id": users[4].id
        },
        {
            "title": "Workshop: Cooperativismo Digital",
            "description": "Atividade educativa sobre transformação digital no cooperativismo e ferramentas tecnológicas.",
            "event_type": EventType.EDUCATIONAL_ACTIVITY,
            "start_date": now + timedelta(days=7),
            "end_date": now + timedelta(days=7, hours=3),
            "location": "Laboratório de Informática",
            "address": "Rua da Cooperação, 500 - Térreo",
            "max_capacity": 30,
            "organizer_id": users[6].id
        },
        {
            "title": "Encontro Mensal dos Aposentados",
            "description": "Encontro social mensal para cooperados aposentados compartilharem experiências e confraternizarem.",
            "event_type": EventType.OTHER,
            "start_date": now + timedelta(days=20),
            "end_date": now + timedelta(days=20, hours=3),
            "location": "Sala de Convivência",
            "address": "Rua da Cooperação, 500 - 1º Andar",
            "max_capacity": 40,
            "organizer_id": users[2].id
        }
    ]
    
    events = []
    for event_data in events_data:
        event = Event(**event_data)
        db.add(event)
        events.append(event)
    
    db.commit()
    
    for event in events:
        db.refresh(event)
    
    print(f"{len(events)} events created!")
    return events

def init_event_registrations(db: Session, users, events):
    print("Creating event registrations...")
    
    registrations_count = 0
    
    # Register some users to each event
    for event in events:
        users_to_register = users[:min(5, len(users))]
        
        for user in users_to_register:
            if user.id != event.organizer_id:  # Organizer doesn't register
                registration = EventRegistration(
                    event_id=event.id,
                    user_id=user.id,
                    attended=False if event.start_date > datetime.now() else True
                )
                db.add(registration)
                registrations_count += 1
    
    db.commit()
    print(f"{registrations_count} event registrations created!")

def init_forum_posts(db: Session, users):
    print("Creating forum posts...")
    
    posts_data = [
        {
            "title": "Dicas para jovens empreendedores iniciantes",
            "content": "Olá pessoal! Gostaria de compartilhar algumas dicas importantes para quem está começando no empreendedorismo:\n\n1. Validem sempre a ideia antes de investir\n2. Conheçam bem o público-alvo\n3. Façam um planejamento financeiro realista\n4. Busquem mentoria de empreendedores experientes\n\nQuais outras dicas vocês dariam?",
            "category": "empreendedorismo",
            "author_id": users[0].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 45,
            "likes_count": 12
        },
        {
            "title": "Como o cooperativismo mudou minha vida",
            "content": "Há 30 anos faço parte desta cooperativa e posso dizer que foi uma das melhores decisões da minha vida. Através do cooperativismo aprendi valores como solidariedade, democracia e responsabilidade social.\n\nVi minha comunidade crescer, meus filhos se desenvolverem com valores sólidos e meu negócio prosperar com o apoio dos cooperados.\n\nGostaria de ouvir outras histórias de como o cooperativismo impactou positivamente a vida de vocês!",
            "category": "experiencias",
            "author_id": users[2].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 67,
            "likes_count": 23
        },
        {
            "title": "Oportunidade de parceria - Agricultura orgânica",
            "content": "Estou buscando parceiros cooperados interessados em investir em agricultura orgânica. Tenho experiência no setor e acesso a terras produtivas.\n\nA ideia é criar uma cooperativa de produção orgânica que atenda tanto o mercado local quanto nacional.\n\nQuem tiver interesse, podem entrar em contato comigo para conversarmos sobre os detalhes do projeto.",
            "category": "negocios",
            "author_id": users[4].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 89,
            "likes_count": 15
        },
        {
            "title": "Educação financeira: Por onde começar?",
            "content": "Muitos cooperados me perguntam por onde começar os estudos em educação financeira. Aqui vai um roteiro básico:\n\n1. Organize suas finanças pessoais\n2. Aprenda sobre orçamento doméstico\n3. Entenda sobre investimentos básicos\n4. Estude sobre previdência e aposentadoria\n5. Conheça os produtos da cooperativa\n\nTenho alguns livros e cursos para recomendar. Quem tiver interesse, posso compartilhar!",
            "category": "educacao-financeira",
            "author_id": users[3].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 134,
            "likes_count": 28
        },
        {
            "title": "Tecnologia no cooperativismo: O futuro é agora",
            "content": "Como jovem cooperada, vejo muitas oportunidades para implementarmos tecnologia em nossos processos. Apps, automação, IA podem revolucionar como fazemos cooperativismo.\n\nGostaria de propor a criação de um grupo de inovação tecnológica na nossa cooperativa. Podemos discutir ideias como:\n\n- App para gestão de benefícios\n- Plataforma de networking entre cooperados\n- Sistema de gamificação para participação\n- Ferramentas de educação financeira digital\n\nQuem toparia participar?",
            "category": "tecnologia",
            "author_id": users[6].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 78,
            "likes_count": 19
        }
    ]
    
    posts = []
    for post_data in posts_data:
        # Adjust publication dates
        post_data["published_at"] = datetime.now() - timedelta(days=len(posts) + 1)
        post = Post(**post_data)
        db.add(post)
        posts.append(post)
    
    db.commit()
    
    for post in posts:
        db.refresh(post)
    
    print(f"{len(posts)} forum posts created!")
    return posts

def init_forum_comments(db: Session, users, posts):
    print("Creating forum comments...")
    
    comments_data = [
        # Comments on entrepreneurship tips post
        {
            "content": "Excelentes dicas! Eu acrescentaria: nunca desistam no primeiro obstáculo. A persistência é fundamental no empreendedorismo.",
            "post_id": posts[0].id,
            "author_id": users[1].id
        },
        {
            "content": "Concordo plenamente! Mentoria foi essencial no meu crescimento. Oferecemos mentoria gratuita na nossa comunidade de jovens empreendedores.",
            "post_id": posts[0].id,
            "author_id": users[4].id
        },
        
        # Comments on cooperativism post
        {
            "content": "Que história inspiradora! O cooperativismo realmente transforma vidas. Estou há 5 anos na cooperativa e já vejo os benefícios.",
            "post_id": posts[1].id,
            "author_id": users[3].id
        },
        {
            "content": "Obrigada por compartilhar sua experiência! Como jovem cooperada, me sinto motivada a continuar participando ativamente.",
            "post_id": posts[1].id,
            "author_id": users[6].id
        },
        
        # Comments on partnership post
        {
            "content": "Interessante projeto! Tenho experiência em marketing digital para produtos orgânicos. Podemos conversar?",
            "post_id": posts[2].id,
            "author_id": users[0].id
        },
        
        # Comments on financial education post
        {
            "content": "Ótimo roteiro! Você poderia recomendar algum livro específico para iniciantes?",
            "post_id": posts[3].id,
            "author_id": users[1].id
        },
        {
            "content": "Recomendo começar com 'Pai Rico, Pai Pobre' e depois partir para livros mais específicos sobre investimentos.",
            "post_id": posts[3].id,
            "author_id": users[3].id,
            "parent_comment_id": None  # Será atualizado após criar o comentário anterior
        },
        
        # Comments on technology post
        {
            "content": "Ideia fantástica! Como desenvolvedor, posso ajudar com a parte técnica. Vamos formar esse grupo!",
            "post_id": posts[4].id,
            "author_id": users[5].id
        },
        {
            "content": "Adorei a proposta! A gamificação pode aumentar muito o engajamento dos cooperados.",
            "post_id": posts[4].id,
            "author_id": users[2].id
        }
    ]
    
    comments = []
    for comment_data in comments_data:
        comment = Comment(**comment_data)
        db.add(comment)
        comments.append(comment)
    
    db.commit()
    
    for comment in comments:
        db.refresh(comment)
    
    # Create a reply to comment (nested comment)
    reply_comment = Comment(
        content="Exatamente! E depois dele, recomendo 'O Investidor Inteligente' do Benjamin Graham.",
        post_id=posts[3].id,
        author_id=users[2].id,
        parent_comment_id=comments[6].id  # Reply to book recommendation comment
    )
    db.add(reply_comment)
    db.commit()
    
    print(f"{len(comments) + 1} forum comments created!")

def main():
    print("Initializing database with mock data...")
    print("=" * 60)
    
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/db", exist_ok=True)
    
    print("Creating tables...")
    create_tables()
    print("Tables created!")
    
    db = SessionLocal()
    
    try:
        users = init_users(db)
        communities = init_communities(db, users)
        init_memberships(db, users, communities)
        events = init_events(db, users)
        init_event_registrations(db, users, events)
        posts = init_forum_posts(db, users)
        init_forum_comments(db, users, posts)
        
        print("=" * 60)
        print("Database initialized successfully!")
        print("\nSummary of created data:")
        print(f"   {len(users)} users")
        print(f"   {len(communities)} communities")
        print(f"   {len(events)} events")
        print(f"   {len(posts)} forum posts")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
