class CommentCreate {
  final String content;
  final int authorId;
  final int postId;

  CommentCreate({
    required this.content,
    required this.authorId,
    required this.postId,
  });

  Map<String, dynamic> toJson() => {
        'content': content,
        'author_id': authorId,
        'post_id': postId,
      };
}
