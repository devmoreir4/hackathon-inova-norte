class Post {
  final int id;
  final String title;
  final String content;
  final int authorId;
  final DateTime createdAt;
  final int likes_count;

  Post({
    required this.id,
    required this.title,
    required this.content,
    required this.authorId,
    required this.createdAt,
    required this.likes_count,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'],
      title: json['title'],
      content: json['content'],
      authorId: json['author_id'],
      createdAt: DateTime.parse(json['created_at']),
      likes_count: json['likes_count'] ?? 0,
    );
  }
}
