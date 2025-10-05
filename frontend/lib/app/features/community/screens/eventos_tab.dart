import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/services/event_service.dart';
import 'package:frontend/app/features/events/widgets/calendar_modal.dart';
import 'package:frontend/app/features/events/widgets/event_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'dart:collection';

class EventosTab extends StatefulWidget {
  const EventosTab({Key? key}) : super(key: key);

  @override
  _EventosTabState createState() => _EventosTabState();
}

class _EventosTabState extends State<EventosTab> {
  final EventService _eventService = EventService();
  List<Event> _allUpcomingEvents = [];
  List<Event> _filteredEvents = [];
  List<String> _eventTypes = [];
  String? _selectedEventType;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchUpcomingEvents();
  }

  Future<void> _fetchUpcomingEvents() async {
    setState(() { _isLoading = true; });
    try {
      final allEvents = await _eventService.getEventsForMonth(DateTime.now().year, DateTime.now().month);
      final upcomingEvents = allEvents.where((e) => e.startDate.isAfter(DateTime.now())).toList();
      final types = LinkedHashSet<String>.from(upcomingEvents.map((e) => e.eventType)).toList();

      setState(() {
        _allUpcomingEvents = upcomingEvents;
        _filteredEvents = upcomingEvents;
        _eventTypes = ['Todos', ...types];
        _selectedEventType = 'Todos';
        _isLoading = false;
      });
    } catch (e) {
      setState(() { _isLoading = false; });
    }
  }

  void _filterEvents(String eventType) {
    setState(() {
      _selectedEventType = eventType;
      if (eventType == 'Todos') {
        _filteredEvents = _allUpcomingEvents;
      } else {
        _filteredEvents = _allUpcomingEvents.where((e) => e.eventType == eventType).toList();
      }
    });
  }

  void _showCalendar() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        expand: false,
        initialChildSize: 0.85,
        maxChildSize: 0.9,
        builder: (_, controller) => const CalendarModal(),
      ),
    );
  }

  String _formatEventType(String eventType) {
    switch (eventType) {
      case 'cooperative_fair': return 'Feira Cooperativa';
      case 'lecture': return 'Palestra';
      case 'business_round': return 'Rodada de Negócios';
      case 'educational_activity': return 'Atividade Educativa';
      case 'Todos': return 'Todos';
      default: return 'Outro';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
          child: ElevatedButton.icon(
            onPressed: _showCalendar,
            icon: const Icon(Icons.calendar_today, color: Color(0xFF003C44)),
            label: const Text('Ver Calendário Completo'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: const Color(0xFF003C44),
              minimumSize: const Size(double.infinity, 48),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
          child: Text(
            'Próximos Eventos',
            style: GoogleFonts.poppins(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
          ),
        ),
        if (_eventTypes.isNotEmpty) _buildEventTypeFilters(),
        Expanded(
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : RefreshIndicator(
                  onRefresh: _fetchUpcomingEvents,
                  child: _filteredEvents.isEmpty
                      ? const Center(
                          child: Text(
                            'Nenhum evento encontrado.',
                            style: TextStyle(color: Colors.white70),
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.only(top: 8),
                          itemCount: _filteredEvents.length,
                          itemBuilder: (context, index) {
                            return EventCard(event: _filteredEvents[index]);
                          },
                        ),
                ),
        ),
      ],
    );
  }

  Widget _buildEventTypeFilters() {
    return SizedBox(
      height: 50,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 12),
        itemCount: _eventTypes.length,
        itemBuilder: (context, index) {
          final type = _eventTypes[index];
          final isSelected = type == _selectedEventType;
          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4.0),
            child: FilterChip(
              label: Text(_formatEventType(type)),
              selected: isSelected,
              onSelected: (selected) => _filterEvents(type),
              backgroundColor: Colors.white.withOpacity(0.1),
              selectedColor: Colors.white,
              labelStyle: TextStyle(
                color: isSelected ? const Color(0xFF003C44) : Colors.white,
                fontWeight: FontWeight.bold,
              ),
              checkmarkColor: const Color(0xFF003C44),
              shape: StadiumBorder(
                side: BorderSide(color: Colors.white.withOpacity(0.3)),
              ),
            ),
          );
        },
      ),
    );
  }
}
