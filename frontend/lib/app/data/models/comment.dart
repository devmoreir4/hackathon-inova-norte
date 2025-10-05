class Comment {
  final int id;
  final String content;
  final int authorId;
  final int postId;
  final DateTime createdAt;

  Comment({
    required this.id,
    required this.content,
    required this.authorId,
    required this.postId,
    required this.createdAt,
  });

  factory Comment.fromJson(Map<String, dynamic> json) {
    return Comment(
      id: json['id'],
      content: json['content'],
      authorId: json['author_id'],
      postId: json['post_id'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
