class PostCreate {
  final String title;
  final String content;
  final String category;
  final int authorId;

  PostCreate({
    required this.title,
    required this.content,
    required this.category,
    required this.authorId,
  });

  Map<String, dynamic> toJson() => {
        'title': title,
        'content': content,
        'category': category,
        'author_id': authorId,
      };
}
