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
    Post, PostStatus, Comment,
    UserLevel, Badge, UserBadge, UserPoints
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
            "name": "Empreendedores Sicoob",
            "description": "Comunidade para empreendedores cooperados compartilharem experiências e oportunidades de negócio.",
            "community_type": CommunityType.PUBLIC,
            "owner_id": users[0].id,
            "max_members": 100,
            "rules": "Respeite todos os membros. Mantenha discussões focadas em empreendedorismo e cooperativismo."
        },
        {
            "name": "Jovens Cooperados",
            "description": "Espaço para jovens cooperados se conectarem e aprenderem sobre cooperativismo.",
            "community_type": CommunityType.PUBLIC,
            "owner_id": users[1].id,
            "max_members": 50,
            "rules": "Comunidade voltada para jovens. Seja respeitoso e construtivo."
        },
        {
            "name": "Educação Financeira",
            "description": "Grupo focado em educação financeira e planejamento para aposentadoria.",
            "community_type": CommunityType.PRIVATE,
            "owner_id": users[2].id,
            "max_members": 200,
            "rules": "Compartilhe conhecimento sobre educação financeira. Evite spam."
        }
    ]
    
    communities = []
    for community_data in communities_data:
        community = Community(**community_data)
        db.add(community)
        communities.append(community)
    
    db.commit()
    for community in communities:
        db.refresh(community)
    
    print(f"{len(communities)} communities created!")
    return communities

def init_community_memberships(db: Session, users, communities):
    print("Creating community memberships...")
    
    memberships_data = [
        # Empreendedores Sicoob community
        {"community_id": communities[0].id, "user_id": users[0].id, "role": MembershipRole.OWNER},
        {"community_id": communities[0].id, "user_id": users[1].id, "role": MembershipRole.MEMBER},
        {"community_id": communities[0].id, "user_id": users[4].id, "role": MembershipRole.MEMBER},
        
        # Jovens Cooperados community
        {"community_id": communities[1].id, "user_id": users[1].id, "role": MembershipRole.OWNER},
        {"community_id": communities[1].id, "user_id": users[0].id, "role": MembershipRole.MEMBER},
        {"community_id": communities[1].id, "user_id": users[3].id, "role": MembershipRole.MEMBER},
        
        # Educação Financeira community
        {"community_id": communities[2].id, "user_id": users[2].id, "role": MembershipRole.OWNER},
        {"community_id": communities[2].id, "user_id": users[0].id, "role": MembershipRole.MEMBER},
        {"community_id": communities[2].id, "user_id": users[3].id, "role": MembershipRole.MEMBER},
        {"community_id": communities[2].id, "user_id": users[4].id, "role": MembershipRole.MEMBER},
    ]
    
    memberships = []
    for membership_data in memberships_data:
        membership = CommunityMembership(**membership_data)
        db.add(membership)
        memberships.append(membership)
    
    db.commit()
    for membership in memberships:
        db.refresh(membership)
    
    print(f"{len(memberships)} community memberships created!")
    return memberships

def init_events(db: Session, users):
    print("Creating events...")
    
    events_data = [
        {
            "title": "Workshop de Educação Financeira",
            "description": "Aprenda sobre planejamento financeiro, investimentos e aposentadoria com especialistas do Sicoob.",
            "event_type": EventType.EDUCATIONAL_ACTIVITY,
            "start_date": datetime.now() + timedelta(days=7),
            "end_date": datetime.now() + timedelta(days=7, hours=3),
            "location": "Auditório Sicoob Centro",
            "address": "Rua das Flores, 123 - Centro",
            "max_capacity": 50,
            "organizer_id": users[0].id
        },
        {
            "title": "Feira de Negócios Cooperativos",
            "description": "Evento para networking entre cooperados empreendedores e apresentação de oportunidades de negócio.",
            "event_type": EventType.COOPERATIVE_FAIR,
            "start_date": datetime.now() + timedelta(days=14),
            "end_date": datetime.now() + timedelta(days=14, hours=6),
            "location": "Centro de Convenções",
            "address": "Av. Principal, 456 - Centro",
            "max_capacity": 100,
            "organizer_id": users[1].id
        },
        {
            "title": "Palestra: O Futuro do Cooperativismo",
            "description": "Discussão sobre tendências e inovações no cooperativismo brasileiro.",
            "event_type": EventType.LECTURE,
            "start_date": datetime.now() + timedelta(days=21),
            "end_date": datetime.now() + timedelta(days=21, hours=2),
            "location": "Sala de Conferências Sicoob",
            "address": "Rua das Palmeiras, 789 - Centro",
            "max_capacity": 30,
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
    
    registrations_data = [
        # Workshop de Educação Financeira
        {"event_id": events[0].id, "user_id": users[0].id, "attended": True, "feedback": "Excelente workshop, aprendi muito sobre investimentos!"},
        {"event_id": events[0].id, "user_id": users[2].id, "attended": True, "feedback": "Muito esclarecedor para planejamento da aposentadoria."},
        {"event_id": events[0].id, "user_id": users[3].id, "attended": False, "feedback": None},
        
        # Feira de Negócios Cooperativos
        {"event_id": events[1].id, "user_id": users[1].id, "attended": True, "feedback": "Ótima oportunidade de networking!"},
        {"event_id": events[1].id, "user_id": users[4].id, "attended": True, "feedback": "Consegui fechar uma parceria importante."},
        {"event_id": events[1].id, "user_id": users[0].id, "attended": False, "feedback": None},
        
        # Palestra: O Futuro do Cooperativismo
        {"event_id": events[2].id, "user_id": users[2].id, "attended": True, "feedback": "Palestra muito inspiradora sobre o futuro do cooperativismo."},
        {"event_id": events[2].id, "user_id": users[1].id, "attended": True, "feedback": "Adorei as discussões sobre tecnologia no cooperativismo."},
    ]
    
    registrations = []
    for registration_data in registrations_data:
        registration = EventRegistration(**registration_data)
        db.add(registration)
        registrations.append(registration)
    
    db.commit()
    for registration in registrations:
        db.refresh(registration)
    
    print(f"{len(registrations)} event registrations created!")
    return registrations

def init_forum_posts(db: Session, users):
    print("Creating forum posts...")
    
    posts_data = [
        {
            "title": "Dicas para economizar no dia a dia",
            "content": "Compartilho algumas estratégias que uso para economizar e investir melhor meu dinheiro. O que vocês fazem para economizar?",
            "category": "educacao-financeira",
            "author_id": users[0].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 45,
            "likes_count": 12,
            "liked_by_user_1": False
        },
        {
            "title": "Oportunidade de parceria - Agricultura orgânica",
            "content": "Estou buscando parceiros cooperados interessados em investir em agricultura orgânica. Tenho experiência no setor e acesso a terras produtivas.\n\nA ideia é criar uma cooperativa de produção orgânica que atenda tanto o mercado local quanto nacional.\n\nQuem tiver interesse, podem entrar em contato comigo para conversarmos sobre os detalhes do projeto.",
            "category": "negocios",
            "author_id": users[4].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 89,
            "likes_count": 15,
            "liked_by_user_1": False
        },
        {
            "title": "Educação financeira: Por onde começar?",
            "content": "Muitos cooperados me perguntam por onde começar os estudos em educação financeira. Aqui vai um roteiro básico:\n\n1. Organize suas finanças pessoais\n2. Aprenda sobre orçamento doméstico\n3. Entenda sobre investimentos básicos\n4. Estude sobre previdência e aposentadoria\n5. Conheça os produtos da cooperativa\n\nTenho alguns livros e cursos para recomendar. Quem tiver interesse, posso compartilhar!",
            "category": "educacao-financeira",
            "author_id": users[3].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 134,
            "likes_count": 28,
            "liked_by_user_1": False
        },
        {
            "title": "Tecnologia no cooperativismo: O futuro é agora",
            "content": "Como jovens cooperados, precisamos estar atentos às inovações tecnológicas que podem revolucionar o cooperativismo.\n\nBlockchain, fintechs, inteligência artificial... Como vocês veem essas tecnologias impactando nosso setor?\n\nVamos discutir ideias e oportunidades!",
            "category": "tecnologia",
            "author_id": users[1].id,
            "status": PostStatus.PUBLISHED,
            "views_count": 67,
            "likes_count": 19,
            "liked_by_user_1": False
        }
    ]
    
    posts = []
    for post_data in posts_data:
        print(f"Creating post with liked_by_user_1: {post_data.get('liked_by_user_1')}")
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
        {
            "post_id": posts[0].id,
            "author_id": users[1].id,
            "content": "Excelente post! Eu também uso a regra dos 50-30-20 para organizar meus gastos. Funciona muito bem!"
        },
        {
            "post_id": posts[0].id,
            "author_id": users[2].id,
            "content": "Ótimas dicas! A dica do controle de gastos por categoria é fundamental. Uso um app para isso."
        },
        {
            "post_id": posts[1].id,
            "author_id": users[0].id,
            "content": "Interessante proposta! Tenho experiência em logística e posso ajudar com a distribuição. Vamos conversar!"
        },
        {
            "post_id": posts[1].id,
            "author_id": users[3].id,
            "content": "Agricultura orgânica é um mercado em crescimento. Boa sorte com o projeto!"
        },
        {
            "post_id": posts[2].id,
            "author_id": users[0].id,
            "content": "Perfeito roteiro! Concordo que começar pela organização pessoal é fundamental."
        },
        {
            "post_id": posts[2].id,
            "author_id": users[4].id,
            "content": "Adorei as dicas! Você poderia me indicar alguns livros sobre investimentos?"
        },
        {
            "post_id": posts[3].id,
            "author_id": users[0].id,
            "content": "Blockchain pode revolucionar a transparência nas cooperativas. Muito interessante!"
        },
        {
            "post_id": posts[3].id,
            "author_id": users[2].id,
            "content": "IA pode ajudar muito na análise de crédito e gestão de riscos. O futuro é promissor!"
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
    
    print(f"{len(comments)} forum comments created!")
    return comments

def init_gamification_badges(db: Session):
    print("Creating gamification badges...")
    
    badges_data = [
        {
            "name": "Primeiro Passo",
            "description": "Criou sua primeira conta no sistema",
            "icon_url": "https://example.com/badges/first-step.png",
            "points_required": 0,
            "category": "welcome"
        },
        {
            "name": "Iniciante do Fórum",
            "description": "Criou seu primeiro post no fórum",
            "icon_url": "https://example.com/badges/forum-beginner.png",
            "points_required": 10,
            "category": "forum"
        },
        {
            "name": "Comentarista Ativo",
            "description": "Fez 10 comentários no fórum",
            "icon_url": "https://example.com/badges/active-commenter.png",
            "points_required": 50,
            "category": "forum"
        },
        {
            "name": "Participante de Eventos",
            "description": "Participou de seu primeiro evento",
            "icon_url": "https://example.com/badges/event-participant.png",
            "points_required": 15,
            "category": "events"
        },
        {
            "name": "Membro da Comunidade",
            "description": "Entrou em sua primeira comunidade",
            "icon_url": "https://example.com/badges/community-member.png",
            "points_required": 8,
            "category": "community"
        },
        {
            "name": "Líder de Comunidade",
            "description": "Criou uma comunidade",
            "icon_url": "https://example.com/badges/community-leader.png",
            "points_required": 20,
            "category": "community"
        },
        {
            "name": "Educador Financeiro",
            "description": "Compartilhou conhecimento sobre educação financeira",
            "icon_url": "https://example.com/badges/financial-educator.png",
            "points_required": 100,
            "category": "education"
        },
        {
            "name": "Empreendedor Ativo",
            "description": "Participou ativamente de discussões sobre negócios",
            "icon_url": "https://example.com/badges/active-entrepreneur.png",
            "points_required": 150,
            "category": "business"
        },
        {
            "name": "Cooperado Exemplar",
            "description": "Alcançou 1000 pontos de experiência",
            "icon_url": "https://example.com/badges/exemplary-member.png",
            "points_required": 1000,
            "category": "achievement"
        },
        {
            "name": "Mentor da Comunidade",
            "description": "Ajudou outros cooperados com conselhos valiosos",
            "icon_url": "https://example.com/badges/community-mentor.png",
            "points_required": 500,
            "category": "mentorship"
        }
    ]
    
    badges = []
    for badge_data in badges_data:
        badge = Badge(**badge_data)
        db.add(badge)
        badges.append(badge)
    
    db.commit()
    for badge in badges:
        db.refresh(badge)
    
    print(f"{len(badges)} badges created!")
    return badges

def init_gamification_data(db: Session, users, posts, events):
    print("Creating gamification data...")
    
    # Create user levels
    user_levels = []
    for i, user in enumerate(users):
        # Give different starting points to make it interesting
        base_points = (i + 1) * 50
        level = UserLevel(
            user_id=user.id,
            level=1,
            experience_points=base_points,
            total_points=base_points
        )
        db.add(level)
        user_levels.append(level)
    
    db.commit()
    for level in user_levels:
        db.refresh(level)
    
    # Create some user points records
    points_data = [
        # User 0 (Ana) - Entrepreneur
        {"user_id": users[0].id, "points": 10, "source": "forum_post", "source_id": posts[0].id, "description": "Criou post sobre economia"},
        {"user_id": users[0].id, "points": 5, "source": "forum_comment", "source_id": posts[1].id, "description": "Comentou em post de negócios"},
        {"user_id": users[0].id, "points": 15, "source": "event_attendance", "source_id": events[0].id, "description": "Participou de workshop"},
        
        # User 1 (Carlos) - Young
        {"user_id": users[1].id, "points": 10, "source": "forum_post", "source_id": posts[3].id, "description": "Criou post sobre tecnologia"},
        {"user_id": users[1].id, "points": 5, "source": "forum_comment", "source_id": posts[0].id, "description": "Comentou em post de educação financeira"},
        {"user_id": users[1].id, "points": 8, "source": "community_join", "source_id": 1, "description": "Entrou na comunidade de jovens"},
        
        # User 2 (Maria) - Retiree
        {"user_id": users[2].id, "points": 5, "source": "forum_comment", "source_id": posts[0].id, "description": "Comentou em post sobre economia"},
        {"user_id": users[2].id, "points": 15, "source": "event_attendance", "source_id": events[2].id, "description": "Participou de palestra"},
        
        # User 3 (João) - General
        {"user_id": users[3].id, "points": 10, "source": "forum_post", "source_id": posts[2].id, "description": "Criou post sobre educação financeira"},
        {"user_id": users[3].id, "points": 5, "source": "forum_comment", "source_id": posts[1].id, "description": "Comentou em post de negócios"},
        
        # User 4 (Patricia) - Entrepreneur
        {"user_id": users[4].id, "points": 10, "source": "forum_post", "source_id": posts[1].id, "description": "Criou post sobre parceria"},
        {"user_id": users[4].id, "points": 5, "source": "forum_comment", "source_id": posts[2].id, "description": "Comentou em post de educação financeira"},
        {"user_id": users[4].id, "points": 20, "source": "community_create", "source_id": 1, "description": "Criou comunidade de empreendedores"},
    ]
    
    user_points = []
    for point_data in points_data:
        point = UserPoints(**point_data)
        db.add(point)
        user_points.append(point)
    
    db.commit()
    for point in user_points:
        db.refresh(point)
    
    print(f"{len(user_points)} user points records created!")
    return user_points

def init_user_badges(db: Session, users, badges):
    print("Creating user badges...")
    
    user_badges_data = [
        # Ana (User 0) - Entrepreneur with high activity
        {"user_id": users[0].id, "badge_id": badges[0].id},  # Primeiro Passo
        {"user_id": users[0].id, "badge_id": badges[1].id},  # Iniciante do Fórum
        {"user_id": users[0].id, "badge_id": badges[3].id},  # Participante de Eventos
        {"user_id": users[0].id, "badge_id": badges[4].id},  # Membro da Comunidade
        {"user_id": users[0].id, "badge_id": badges[6].id},  # Educador Financeiro
        
        # Carlos (User 1) - Young with tech focus
        {"user_id": users[1].id, "badge_id": badges[0].id},  # Primeiro Passo
        {"user_id": users[1].id, "badge_id": badges[1].id},  # Iniciante do Fórum
        {"user_id": users[1].id, "badge_id": badges[3].id},  # Participante de Eventos
        {"user_id": users[1].id, "badge_id": badges[4].id},  # Membro da Comunidade
        
        # Maria (User 2) - Retiree with education focus
        {"user_id": users[2].id, "badge_id": badges[0].id},  # Primeiro Passo
        {"user_id": users[2].id, "badge_id": badges[3].id},  # Participante de Eventos
        {"user_id": users[2].id, "badge_id": badges[4].id},  # Membro da Comunidade
        
        # João (User 3) - General user
        {"user_id": users[3].id, "badge_id": badges[0].id},  # Primeiro Passo
        {"user_id": users[3].id, "badge_id": badges[1].id},  # Iniciante do Fórum
        {"user_id": users[3].id, "badge_id": badges[4].id},  # Membro da Comunidade
        
        # Patricia (User 4) - Entrepreneur with business focus
        {"user_id": users[4].id, "badge_id": badges[0].id},  # Primeiro Passo
        {"user_id": users[4].id, "badge_id": badges[1].id},  # Iniciante do Fórum
        {"user_id": users[4].id, "badge_id": badges[4].id},  # Membro da Comunidade
        {"user_id": users[4].id, "badge_id": badges[5].id},  # Líder de Comunidade
        {"user_id": users[4].id, "badge_id": badges[7].id},  # Empreendedor Ativo
    ]
    
    user_badges = []
    for user_badge_data in user_badges_data:
        user_badge = UserBadge(**user_badge_data)
        db.add(user_badge)
        user_badges.append(user_badge)
    
    db.commit()
    for user_badge in user_badges:
        db.refresh(user_badge)
    
    print(f"{len(user_badges)} user badges created!")
    return user_badges

def main():
    print("Initializing database with sample data...")
    
    # Create tables
    create_tables()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Initialize data
        users = init_users(db)
        communities = init_communities(db, users)
        community_memberships = init_community_memberships(db, users, communities)
        events = init_events(db, users)
        event_registrations = init_event_registrations(db, users, events)
        posts = init_forum_posts(db, users)
        comments = init_forum_comments(db, users, posts)
        badges = init_gamification_badges(db)
        user_badges = init_user_badges(db, users, badges)
        gamification_data = init_gamification_data(db, users, posts, events)
        
        print("\nDatabase initialization completed successfully!")
        print(f"Summary:")
        print(f"   - Users: {len(users)}")
        print(f"   - Communities: {len(communities)}")
        print(f"   - Community Memberships: {len(community_memberships)}")
        print(f"   - Events: {len(events)}")
        print(f"   - Event Registrations: {len(event_registrations)}")
        print(f"   - Forum Posts: {len(posts)}")
        print(f"   - Forum Comments: {len(comments)}")
        print(f"   - Badges: {len(badges)}")
        print(f"   - User Badges: {len(user_badges)}")
        print(f"   - Gamification Records: {len(gamification_data)}")
        
    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()