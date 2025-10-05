import 'dart:collection';
import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/services/event_service.dart';
import 'package:frontend/app/features/events/widgets/event_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:table_calendar/table_calendar.dart';

class EventosTab extends StatefulWidget {
  const EventosTab({Key? key}) : super(key: key);

  @override
  _EventosTabState createState() => _EventosTabState();
}

class _EventosTabState extends State<EventosTab> {
  final EventService _eventService = EventService();
  
  // State variables
  List<Event> _allUpcomingEvents = [];
  late ValueNotifier<List<Event>> _displayedEvents;
  LinkedHashMap<DateTime, List<Event>> _allEventsByDay = LinkedHashMap();
  List<String> _eventTypes = [];
  String? _selectedFilter;
  Map<int, int> _myRegistrations = {}; // Map<eventId, registrationId>

  // Calendar state
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;
  CalendarFormat _calendarFormat = CalendarFormat.month;

  @override
  void initState() {
    super.initState();
    _displayedEvents = ValueNotifier([]);
    _fetchAndSetInitialEvents();
  }

  @override
  void dispose() {
    _displayedEvents.dispose();
    super.dispose();
  }

  Future<void> _fetchAndSetInitialEvents() async {
    try {
      const userId = 1; // Placeholder for logged-in user
      final results = await Future.wait([
        _eventService.getAllEvents(),
        _eventService.getRegistrationsForUser(userId),
      ]);

      final allEvents = results[0] as List<Event>;
      final registrations = results[1] as List<dynamic>;

      if (!mounted) return;

      _allEventsByDay = _groupEventsByDay(allEvents);
      _allUpcomingEvents = allEvents.where((e) => e.startDate.isAfter(DateTime.now())).toList();
      final types = LinkedHashSet<String>.from(_allUpcomingEvents.map((e) => e.eventType)).toList();
      _myRegistrations = {for (var reg in registrations) reg.eventId: reg.id};
      
      setState(() {
        _eventTypes = ['Todos', 'Inscrito', ...types]; // Add 'Inscrito' filter
        _selectedFilter = 'Todos';
        _applyFilters();
      });

    } catch (e) {
      // handle error
    }
  }

  void _selectFilter(String filter) {
    setState(() {
      _selectedFilter = filter;
      _applyFilters();
    });
  }

  void _onDaySelected(DateTime selectedDay, DateTime focusedDay) {
    setState(() {
      _focusedDay = focusedDay;
      if (isSameDay(_selectedDay, selectedDay)) {
        _selectedDay = null; // Clear day filter
      } else {
        _selectedDay = selectedDay;
      }
      _applyFilters();
    });
  }

  void _applyFilters() {
    List<Event> events = _allUpcomingEvents;

    // Filter by selected chip
    if (_selectedFilter != null) {
      if (_selectedFilter == 'Inscrito') {
        events = events.where((e) => _myRegistrations.containsKey(e.id)).toList();
      } else if (_selectedFilter != 'Todos') {
        events = events.where((e) => e.eventType == _selectedFilter).toList();
      }
    }

    // Then, filter by selected day (if any)
    if (_selectedDay != null) {
      final dayEvents = _getEventsForDay(_selectedDay!);
      events = events.where((e) => dayEvents.contains(e)).toList();
    }

    _displayedEvents.value = events;
  }

  LinkedHashMap<DateTime, List<Event>> _groupEventsByDay(List<Event> events) {
    final map = LinkedHashMap<DateTime, List<Event>>();
    for (var event in events) {
      final day = DateTime.utc(event.startDate.year, event.startDate.month, event.startDate.day);
      (map[day] ??= []).add(event);
    }
    return map;
  }

  List<Event> _getEventsForDay(DateTime day) {
    final utcDay = DateTime.utc(day.year, day.month, day.day);
    return _allEventsByDay[utcDay] ?? [];
  }

  String _formatFilterName(String filter) {
    switch (filter) {
      case 'cooperative_fair': return 'Feira';
      case 'lecture': return 'Palestra';
      case 'business_round': return 'Negócios';
      case 'educational_activity': return 'Educativo';
      case 'Todos': return 'Todos';
      case 'Inscrito': return 'Inscrito';
      default: return 'Outro';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildEventTypeFilters(),
        Padding(
          padding: const EdgeInsets.fromLTRB(8, 0, 8, 8),
          child: Card(
            elevation: 2,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: ExpansionTile(
              title: Text(
                'Exibir Calendário de Eventos',
                style: GoogleFonts.poppins(fontWeight: FontWeight.bold, color: const Color(0xFFFFFFFF)),
              ),
              leading: const Icon(Icons.calendar_today, color: Color(0xFF003C44)),
              iconColor: const Color(0xFF003C44),
              collapsedIconColor: const Color(0xFF003C44),
              children: [
                TableCalendar<Event>(
                  locale: 'pt_BR',
                  firstDay: DateTime.utc(2020, 1, 1),
                  lastDay: DateTime.utc(2030, 12, 31),
                  focusedDay: _focusedDay,
                  selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
                  calendarFormat: _calendarFormat,
                  eventLoader: _getEventsForDay,
                  startingDayOfWeek: StartingDayOfWeek.monday,
                  onDaySelected: _onDaySelected,
                  onPageChanged: (focusedDay) {
                    _focusedDay = focusedDay;
                  },
                  onFormatChanged: (format) {
                    if (_calendarFormat != format) {
                      setState(() {
                        _calendarFormat = format;
                      });
                    }
                  },
                  calendarStyle: CalendarStyle(
                    outsideDaysVisible: false,
                    todayDecoration: BoxDecoration(
                      color: const Color(0xFF00838A).withOpacity(0.5),
                      shape: BoxShape.circle,
                    ),
                    selectedDecoration: const BoxDecoration(
                      color: Color(0xFF00838A),
                      shape: BoxShape.circle,
                    ),
                    markerDecoration: const BoxDecoration(
                      color: Color(0xFF98CE00),
                      shape: BoxShape.circle,
                    ),
                  ),
                  headerStyle: HeaderStyle(
                    titleCentered: true,
                    formatButtonShowsNext: false,
                    titleTextStyle: GoogleFonts.poppins(fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                ),
              ],
            ),
          ),
        ),
        Expanded(
          child: ValueListenableBuilder<List<Event>>(
            valueListenable: _displayedEvents,
            builder: (context, value, _) {
              if (value.isEmpty) {
                return const Center(
                  child: Text(
                    "Nenhum evento encontrado.",
                    style: TextStyle(color: Colors.white70),
                  ),
                );
              }
              return RefreshIndicator(
                onRefresh: _fetchAndSetInitialEvents,
                child: ListView.builder(
                  itemCount: value.length,
                  itemBuilder: (context, index) {
                    final event = value[index];
                    final isRegistered = _myRegistrations.containsKey(event.id);
                    return EventCard(
                      event: event,
                      isRegistered: isRegistered,
                      onStatusChanged: _fetchAndSetInitialEvents,
                    );
                  },
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildEventTypeFilters() {
    if (_eventTypes.isEmpty) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(top: 16.0, bottom: 8.0),
      child: SizedBox(
        height: 50,
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 12),
          itemCount: _eventTypes.length,
          itemBuilder: (context, index) {
            final type = _eventTypes[index];
            final isSelected = type == _selectedFilter;
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4.0),
              child: FilterChip(
                label: Text(_formatFilterName(type)),
                selected: isSelected,
                onSelected: (selected) => _selectFilter(type),
                backgroundColor: Colors.white.withOpacity(0.1),
                selectedColor: Colors.white,
                labelStyle: TextStyle(
                  color: isSelected ? const Color(0xFF003C44) : Colors.white,
                  fontWeight: FontWeight.bold,
                ),
                checkmarkColor: const Color(0xFF003C44),
                shape: const StadiumBorder(),
              ),
            );
          },
        ),
      ),
    );
  }
}
