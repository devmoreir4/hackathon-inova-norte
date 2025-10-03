
class Community {
  final int id;
  final String name;
  final String description;
  final int ownerId;
  final String communityType;
  final int memberCount;
  final DateTime createdAt;
  final DateTime updatedAt;

  Community({
    required this.id,
    required this.name,
    required this.description,
    required this.ownerId,
    required this.communityType,
    required this.memberCount,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Community.fromJson(Map<String, dynamic> json) {
    return Community(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      ownerId: json['owner_id'],
      communityType: json['community_type'],
      memberCount: json['member_count'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }
}
