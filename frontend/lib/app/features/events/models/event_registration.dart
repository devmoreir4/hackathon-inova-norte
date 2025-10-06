class EventRegistration {
  final int id;
  final int eventId;
  final int userId;
  final DateTime registeredAt;
  final bool attended;
  final String? feedback;

  EventRegistration({
    required this.id,
    required this.eventId,
    required this.userId,
    required this.registeredAt,
    required this.attended,
    this.feedback,
  });

  factory EventRegistration.fromJson(Map<String, dynamic> json) {
    return EventRegistration(
      id: json['id'],
      eventId: json['event_id'],
      userId: json['user_id'],
      registeredAt: DateTime.parse(json['registered_at']),
      attended: json['attended'],
      feedback: json['feedback'],
    );
  }
}
