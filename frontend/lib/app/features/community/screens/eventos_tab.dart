import 'dart:collection';
import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/services/event_service.dart';
import 'package:frontend/app/features/events/widgets/event_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:table_calendar/table_calendar.dart';

class EventosTab extends StatefulWidget {
  const EventosTab({Key? key}) : super(key: key);

  @override
  _EventosTabState createState() => _EventosTabState();
}

class _EventosTabState extends State<EventosTab> {
  final EventService _eventService = EventService();
  late final ValueNotifier<List<Event>> _displayedEvents;
  LinkedHashMap<DateTime, List<Event>> _allEventsByDay = LinkedHashMap();
  List<Event> _allUpcomingEvents = [];

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
      final allEvents = await _eventService.getAllEvents();
      if (!mounted) return;

      _allEventsByDay = _groupEventsByDay(allEvents);
      _allUpcomingEvents = allEvents.where((e) => e.startDate.isAfter(DateTime.now())).toList();
      
      setState(() {
        _displayedEvents.value = _allUpcomingEvents;
        _selectedDay = null; // Start with no day selected
      });

    } catch (e) {
      // handle error
    }
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

  void _onDaySelected(DateTime selectedDay, DateTime focusedDay) {
    setState(() {
      _focusedDay = focusedDay;
      // If the user taps the same day again, clear the filter
      if (isSameDay(_selectedDay, selectedDay)) {
        _selectedDay = null;
        _displayedEvents.value = _allUpcomingEvents;
      } else {
        _selectedDay = selectedDay;
        _displayedEvents.value = _getEventsForDay(selectedDay);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
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
                    // No need to fetch on page change as we have all events
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
        const SizedBox(height: 8.0),
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
                    return EventCard(event: value[index]);
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
