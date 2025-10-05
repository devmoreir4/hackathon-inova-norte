class Event {
  final int id;
  final String title;
  final String description;
  final String eventType;
  final DateTime startDate;
  final DateTime? endDate;
  final String location;
  final String? address;
  final int? maxCapacity;
  final bool registrationsOpen;
  final int organizerId;
  final DateTime createdAt;

  Event({
    required this.id,
    required this.title,
    required this.description,
    required this.eventType,
    required this.startDate,
    this.endDate,
    required this.location,
    this.address,
    this.maxCapacity,
    required this.registrationsOpen,
    required this.organizerId,
    required this.createdAt,
  });

  factory Event.fromJson(Map<String, dynamic> json) {
    return Event(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      eventType: json['event_type'],
      startDate: DateTime.parse(json['start_date']),
      endDate: json['end_date'] != null ? DateTime.parse(json['end_date']) : null,
      location: json['location'],
      address: json['address'],
      maxCapacity: json['max_capacity'],
      registrationsOpen: json['registrations_open'],
      organizerId: json['organizer_id'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
