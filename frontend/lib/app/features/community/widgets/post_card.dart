import 'package:flutter/material.dart';
import 'package:frontend/app/data/models/post.dart';
import 'package:frontend/app/data/models/user.dart';
import 'package:frontend/app/data/services/user_service.dart';
import 'package:frontend/app/data/models/comment.dart';
import 'package:frontend/app/data/services/forum_service.dart';
import 'package:frontend/app/features/community/screens/post_details_screen.dart';
import 'package:share_plus/share_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

class PostCard extends StatefulWidget {
  final Post post;

  const PostCard({super.key, required this.post});

  @override
  State<PostCard> createState() => _PostCardState();
}

class _PostCardState extends State<PostCard> {
  late Future<User> _author;
  late Post _currentPost;
  final ForumService _forumService = ForumService();
  late SharedPreferences _prefs;
  bool _isLikedLocally = false; // Local state for heart icon
  final GlobalKey<_CommentCountWidgetState> _commentCountWidgetKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    _author = UserService().getUser(widget.post.authorId);
    _currentPost = widget.post;
    _loadLikeStatus();
  }

  Future<void> _loadLikeStatus() async {
    _prefs = await SharedPreferences.getInstance();
    setState(() {
      _isLikedLocally = _prefs.getBool('post_like_${_currentPost.id}') ?? false;
    });
  }

  Future<void> _toggleLike() async {
    try {
      final updatedPost = await _forumService.likePost(_currentPost.id);
      setState(() {
        _currentPost = updatedPost;
        _isLikedLocally = !_isLikedLocally; // Toggle local state
        _prefs.setBool('post_like_${_currentPost.id}', _isLikedLocally);
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to like post: $e')),
      );
    }
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
              _currentPost.title,
              style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              _currentPost.content,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontSize: 15),
            ),
            const SizedBox(height: 8),
            TextButton(
              onPressed: () async {
                final commentAdded = await Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => PostDetailsScreen(post: _currentPost, openKeyboard: false),
                  ),
                );
                if (commentAdded == true) {
                  _commentCountWidgetKey.currentState?._fetchComments();
                }
              },
              child: const Text('Continuar lendo', style: TextStyle(color: Color(0xFF007A8D))),
            ),
            const Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    IconButton(
                      icon: Icon(
                        _isLikedLocally ? Icons.favorite : Icons.favorite_border,
                        color: _isLikedLocally ? Colors.red : null,
                      ),
                      onPressed: _toggleLike,
                      tooltip: 'Curtir post',
                    ),
                    Text('${_currentPost.likes_count}'),
                  ],
                ),
                Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.comment_outlined),
                      onPressed: () async {
                        final commentAdded = await Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => PostDetailsScreen(post: _currentPost, openKeyboard: true),
                          ),
                        );
                        if (commentAdded == true) {
                          _commentCountWidgetKey.currentState?._fetchComments();
                        }
                      },
                    ),
                    _CommentCountWidget(key: _commentCountWidgetKey, postId: _currentPost.id),
                  ],
                ),
                IconButton(icon: const Icon(Icons.send_outlined), onPressed: () {
                  Share.share('${_currentPost.title}\n${_currentPost.content}');
                }),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _CommentCountWidget extends StatefulWidget {
  final int postId;
  final VoidCallback? onRefresh; // Added callback

  const _CommentCountWidget({super.key, required this.postId, this.onRefresh});

  @override
  State<_CommentCountWidget> createState() => _CommentCountWidgetState();
}

class _CommentCountWidgetState extends State<_CommentCountWidget> {
  late Future<List<Comment>> _comments;
  final ForumService _forumService = ForumService();

  @override
  void initState() {
    super.initState();
    _fetchComments();
  }

  // Method to fetch comments
  void _fetchComments() {
    setState(() {
      _comments = _forumService.getComments(widget.postId);
    });
  }

  @override
  void didUpdateWidget(covariant _CommentCountWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.onRefresh != oldWidget.onRefresh) {
      // If the callback changes, it might indicate a refresh is needed
      // Or, more directly, the parent can call a method on this state.
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Comment>>(
      future: _comments,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Text('...');
        } else if (snapshot.hasError) {
          return const Text('Erro');
        } else if (snapshot.hasData) {
          return Text('${snapshot.data!.length}');
        } else {
          return const Text('0');
        }
      },
    );
  }
}
