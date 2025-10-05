class Post {
  final int id;
  final String title;
  final String content;
  final int authorId;
  final DateTime createdAt;
  final int likes_count;
  final bool liked_by_user_1;

  Post({
    required this.id,
    required this.title,
    required this.content,
    required this.authorId,
    required this.createdAt,
    required this.likes_count,
    required this.liked_by_user_1,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'],
      title: json['title'],
      content: json['content'],
      authorId: json['author_id'],
      createdAt: DateTime.parse(json['created_at']),
      likes_count: json['likes_count'] ?? 0,
      liked_by_user_1: json['liked_by_user_1'] ?? false,
    );
  }
}
