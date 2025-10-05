import 'package:flutter/foundation.dart';

class Course {
  final int id;
  final String title;
  final String description;
  final String category;
  final int pointsReward;
  final String? imageUrl;
  final String? videoUrl;
  final String? content;
  final int instructorId;
  final DateTime createdAt;
  final DateTime? updatedAt;

  Course({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required this.pointsReward,
    this.imageUrl,
    this.videoUrl,
    this.content,
    required this.instructorId,
    required this.createdAt,
    this.updatedAt,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      category: json['category'],
      pointsReward: json['points_reward'],
      imageUrl: json['image_url'],
      videoUrl: json['video_url'],
      content: json['content'],
      instructorId: json['instructor_id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
    );
  }
}
