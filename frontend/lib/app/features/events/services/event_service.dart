import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/models/event_registration.dart';

class EventService {
  final String _baseUrl = 'http://192.168.1.7:5000/api/v1'; // Using the correct IP and port

  Future<List<Event>> getEventsForMonth(int year, int month) async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/events/calendar/month/$year/$month'));

      if (response.statusCode == 200) {
        List<dynamic> body = json.decode(utf8.decode(response.bodyBytes));
        List<Event> events = body.map((dynamic item) => Event.fromJson(item)).toList();
        return events;
      } else {
        throw Exception('Failed to load events for month. Status code: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to load events: $e');
    }
  }

  Future<List<Event>> getAllEvents() async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/events'));

      if (response.statusCode == 200) {
        List<dynamic> body = json.decode(utf8.decode(response.bodyBytes));
        List<Event> events = body.map((dynamic item) => Event.fromJson(item)).toList();
        return events;
      } else {
        throw Exception('Failed to load all events. Status code: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to load all events: $e');
    }
  }

  Future<List<EventRegistration>> getRegistrationsForUser(int userId) async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/events/user/$userId/registrations'));
      if (response.statusCode == 200) {
        List<dynamic> body = json.decode(utf8.decode(response.bodyBytes));
        return body.map((dynamic item) => EventRegistration.fromJson(item)).toList();
      } else {
        throw Exception('Failed to load user registrations');
      }
    } catch (e) {
      throw Exception('Failed to load user registrations: $e');
    }
  }

  Future<void> registerForEvent(int eventId, int userId) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/events/$eventId/register?user_id=$userId'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'event_id': eventId}),
    );

    if (response.statusCode != 201) {
      String detail = 'Ocorreu um erro.'; // Default error message
      try {
        final decoded = json.decode(utf8.decode(response.bodyBytes));
        detail = decoded['detail'] ?? detail;
      } catch (_) {
        // Keep default error message if parsing fails
      }
      throw detail;
    }
  }

  Future<void> unregisterFromEvent(int eventId, int registrationId) async {
    final response = await http.delete(
      Uri.parse('$_baseUrl/events/$eventId/registrations/$registrationId'),
    );

    if (response.statusCode != 204) {
      throw Exception('Failed to unregister from event');
    }
  }
}
