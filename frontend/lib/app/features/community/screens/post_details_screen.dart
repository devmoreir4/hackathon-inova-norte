import 'package:flutter/material.dart';
import 'package:frontend/app/data/models/post.dart';
import 'package:frontend/app/data/models/comment.dart';
import 'package:frontend/app/data/models/comment_create.dart';
import 'package:frontend/app/data/models/user.dart';
import 'package:frontend/app/data/services/forum_service.dart';
import 'package:frontend/app/data/services/user_service.dart';

class PostDetailsScreen extends StatefulWidget {
  final Post post;

  const PostDetailsScreen({super.key, required this.post});

  @override
  State<PostDetailsScreen> createState() => _PostDetailsScreenState();
}

class _PostDetailsScreenState extends State<PostDetailsScreen> {
  late Future<User> _author;
  late Future<List<Comment>> _comments;
  final _commentController = TextEditingController();
  final ForumService _forumService = ForumService();
  final UserService _userService = UserService();

  @override
  void initState() {
    super.initState();
    _author = _userService.getUser(widget.post.authorId);
    _comments = _forumService.getComments(widget.post.id);
  }

  Future<void> _submitComment() async {
    if (_commentController.text.isEmpty) return;

    final newComment = CommentCreate(
      content: _commentController.text,
      authorId: 1, // Hardcoded for now
      postId: widget.post.id,
    );

    try {
      await _forumService.createComment(newComment);
      _commentController.clear();
      setState(() {
        _comments = _forumService.getComments(widget.post.id);
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to create comment: $e')),
      );
    }
  }

  @override
  void dispose() {
    _commentController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalhes do Post'),
        backgroundColor: const Color(0xFF003C44),
      ),
      body: Container(
        color: const Color(0xFF04575c),
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    FutureBuilder<User>(
                      future: _author,
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return const Text('Carregando autor...', style: TextStyle(color: Colors.white));
                        } else if (snapshot.hasError) {
                          return Text('Erro ao carregar autor: ${snapshot.error}', style: const TextStyle(color: Colors.white));
                        } else if (snapshot.hasData) {
                          return Text(
                            'Por: ${snapshot.data!.name}',
                            style: const TextStyle(color: Colors.white70, fontSize: 14),
                          );
                        } else {
                          return const Text('Autor desconhecido', style: TextStyle(color: Colors.white));
                        }
                      },
                    ),
                    const SizedBox(height: 8.0),
                    Text(
                      widget.post.title,
                      style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16.0),
                    Text(
                      widget.post.content,
                      style: const TextStyle(color: Colors.white, fontSize: 16),
                    ),
                    const SizedBox(height: 24.0),
                    const Text(
                      'Comentários',
                      style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const Divider(color: Colors.white70),
                    FutureBuilder<List<Comment>>(
                      future: _comments,
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return const Center(child: CircularProgressIndicator());
                        } else if (snapshot.hasError) {
                          return Center(child: Text('Erro ao carregar comentários: ${snapshot.error}', style: const TextStyle(color: Colors.white)));
                        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                          return const Center(child: Text('Nenhum comentário ainda.', style: TextStyle(color: Colors.white)));
                        } else {
                          return ListView.builder(
                            shrinkWrap: true,
                            physics: const NeverScrollableScrollPhysics(),
                            itemCount: snapshot.data!.length,
                            itemBuilder: (context, index) {
                              final comment = snapshot.data![index];
                              return FutureBuilder<User>(
                                future: _userService.getUser(comment.authorId),
                                builder: (context, userSnapshot) {
                                  if (userSnapshot.connectionState == ConnectionState.waiting) {
                                    return const Text('Carregando comentário...', style: TextStyle(color: Colors.white));
                                  } else if (userSnapshot.hasError) {
                                    return Text('Erro ao carregar autor do comentário: ${userSnapshot.error}', style: const TextStyle(color: Colors.white));
                                  } else if (userSnapshot.hasData) {
                                    return Card(
                                      margin: const EdgeInsets.symmetric(vertical: 4.0),
                                      child: Padding(
                                        padding: const EdgeInsets.all(8.0),
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(userSnapshot.data!.name, style: const TextStyle(fontWeight: FontWeight.bold)),
                                            const SizedBox(height: 4.0),
                                            Text(comment.content),
                                          ],
                                        ),
                                      ),
                                    );
                                  } else {
                                    return const Text('Autor do comentário desconhecido', style: TextStyle(color: Colors.white));
                                  }
                                },
                              );
                            },
                          );
                        }
                      },
                    ),
                  ],
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _commentController,
                      style: const TextStyle(color: Colors.black),
                      decoration: InputDecoration(
                        hintText: 'Faça um comentário...',
                        hintStyle: const TextStyle(color: Colors.grey),
                        filled: true,
                        fillColor: Colors.white,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30.0),
                          borderSide: BorderSide.none,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8.0),
                  FloatingActionButton(
                    onPressed: _submitComment,
                    mini: true,
                    child: const Icon(Icons.send),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
