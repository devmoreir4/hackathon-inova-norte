import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/services/event_service.dart';
import 'package:frontend/app/features/events/widgets/calendar_modal.dart';
import 'package:frontend/app/features/events/widgets/event_card.dart';
import 'package:google_fonts/google_fonts.dart';

class EventosTab extends StatefulWidget {
  const EventosTab({Key? key}) : super(key: key);

  @override
  _EventosTabState createState() => _EventosTabState();
}

class _EventosTabState extends State<EventosTab> {
  final EventService _eventService = EventService();
  late Future<List<Event>> _upcomingEventsFuture;

  @override
  void initState() {
    super.initState();
    _upcomingEventsFuture = _fetchUpcomingEvents();
  }

  Future<List<Event>> _fetchUpcomingEvents() {
    // For simplicity, we fetch all events and filter for upcoming ones in the client.
    // In a real app, the backend should have an endpoint for this.
    return _eventService.getEventsForMonth(DateTime.now().year, DateTime.now().month)
        .then((events) => events.where((e) => e.startDate.isAfter(DateTime.now())).toList());
  }

  Future<void> _refreshEvents() async {
    setState(() {
      _upcomingEventsFuture = _fetchUpcomingEvents();
    });
  }

  void _showCalendar() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        expand: false,
        initialChildSize: 0.8,
        maxChildSize: 0.9,
        builder: (_, controller) => const CalendarModal(), // This needs to be adapted
      ),
    );
  }

  void _register(int eventId) {
    const userId = 1; // Placeholder
    _eventService.registerForEvent(eventId, userId).then((_) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Inscrição realizada com sucesso!')),
      );
    }).catchError((e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erro na inscrição: $e')),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: ElevatedButton.icon(
            onPressed: _showCalendar,
            icon: const Icon(Icons.calendar_today, color: Color(0xFF003C44)),
            label: const Text('Ver Calendário Completo'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: const Color(0xFF003C44),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Text(
            'Próximos Eventos',
            style: GoogleFonts.poppins(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
          ),
        ),
        Expanded(
          child: FutureBuilder<List<Event>>(
            future: _upcomingEventsFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError || !snapshot.hasData || snapshot.data!.isEmpty) {
                return const Center(
                  child: Text(
                    'Nenhum evento futuro encontrado.',
                    style: TextStyle(color: Colors.white70),
                  ),
                );
              }
              final events = snapshot.data!;
              return RefreshIndicator(
                onRefresh: _refreshEvents,
                child: ListView.builder(
                  padding: const EdgeInsets.only(top: 8),
                  itemCount: events.length,
                  itemBuilder: (context, index) {
                    return EventCard(event: events[index]);
                  },
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
