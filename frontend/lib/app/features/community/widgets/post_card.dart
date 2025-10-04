import 'package:flutter/material.dart';
import 'package:frontend/app/data/models/post.dart';
import 'package:frontend/app/data/models/user.dart';
import 'package:frontend/app/data/services/user_service.dart';
import 'package:frontend/app/features/community/screens/post_details_screen.dart';

class PostCard extends StatefulWidget {
  final Post post;

  const PostCard({super.key, required this.post});

  @override
  State<PostCard> createState() => _PostCardState();
}

class _PostCardState extends State<PostCard> {
  late Future<User> _author;

  @override
  void initState() {
    super.initState();
    _author = UserService().getUser(widget.post.authorId);
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
      elevation: 2.0, // Subtle shadow
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            FutureBuilder<User>(
              future: _author,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Row(
                    children: [
                      CircleAvatar(radius: 15), // Placeholder
                      SizedBox(width: 8),
                      Text('Loading...'),
                    ],
                  );
                } else if (snapshot.hasError) {
                  return const Text('Error loading author');
                } else if (snapshot.hasData) {
                  return Row(
                    children: [
                      const CircleAvatar(radius: 15, child: Icon(Icons.person)),
                      const SizedBox(width: 8),
                      Text(
                        snapshot.data!.name,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      ),
                      const Spacer(),
                      const Icon(Icons.bookmark_border),
                    ],
                  );
                } else {
                  return const Text('Author not found');
                }
              },
            ),
            const SizedBox(height: 12),
            Text(
              widget.post.title,
              style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              widget.post.content,
              maxLines: 3,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontSize: 15),
            ),
            const SizedBox(height: 8),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => PostDetailsScreen(post: widget.post, openKeyboard: false),
                  ),
                );
              },
              child: const Text('Continuar lendo', style: TextStyle(color: Color(0xFF007A8D))),
            ),
            const Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                IconButton(
                  icon: const Icon(Icons.favorite_border),
                  onPressed: null, // Disabled because no API endpoint for likes
                  tooltip: 'Funcionalidade de like não disponível',
                ),
                IconButton(
                  icon: const Icon(Icons.comment_outlined),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => PostDetailsScreen(post: widget.post, openKeyboard: true),
                      ),
                    );
                  },
                ),
                IconButton(icon: const Icon(Icons.send_outlined), onPressed: () {}),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
