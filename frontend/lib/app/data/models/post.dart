class Post {
  final int id;
  final String title;
  final String content;
  final int authorId;
  final DateTime createdAt;

  Post({
    required this.id,
    required this.title,
    required this.content,
    required this.authorId,
    required this.createdAt,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'],
      title: json['title'],
      content: json['content'],
      authorId: json['author_id'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
