import 'package:flutter/material.dart';
import 'package:frontend/app/data/models/post.dart';
import 'package:frontend/app/data/services/forum_service.dart';
import 'package:frontend/app/features/community/widgets/post_card.dart';

class ForumTab extends StatefulWidget {
  const ForumTab({super.key});

  @override
  State<ForumTab> createState() => _ForumTabState();
}

class _ForumTabState extends State<ForumTab> {
  late Future<List<Post>> _posts;

  @override
  void initState() {
    super.initState();
    _posts = ForumService().getPosts();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Crie algo...',
              filled: true,
              fillColor: Colors.white,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30.0),
                borderSide: BorderSide.none,
              ),
            ),
          ),
        ),
        const Text(
          '💡 Seja ativo e ganhe pontos Coopera!',
          style: TextStyle(color: Colors.white),
        ),
        Expanded(
          child: FutureBuilder<List<Post>>(
            future: _posts,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              } else if (snapshot.hasError) {
                return Center(child: Text('Error: ${snapshot.error}'));
              } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                return const Center(child: Text('No posts found.'));
              } else {
                return ListView.builder(
                  itemCount: snapshot.data!.length,
                  itemBuilder: (context, index) {
                    return PostCard(post: snapshot.data![index]);
                  },
                );
              }
            },
          ),
        ),
      ],
    );
  }
}
