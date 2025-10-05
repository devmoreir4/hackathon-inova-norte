import 'dart:collection';
import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/services/event_service.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:table_calendar/table_calendar.dart';

class CalendarModal extends StatefulWidget {
  const CalendarModal({Key? key}) : super(key: key);

  @override
  _CalendarModalState createState() => _CalendarModalState();
}

class _CalendarModalState extends State<CalendarModal> {
  final EventService _eventService = EventService();
  late final ValueNotifier<List<Event>> _selectedEvents;
  LinkedHashMap<DateTime, List<Event>> _monthlyEvents = LinkedHashMap();

  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;

  @override
  void initState() {
    super.initState();
    _selectedDay = _focusedDay;
    _selectedEvents = ValueNotifier(_getEventsForDay(_selectedDay!));
    _fetchEventsForMonth(_focusedDay);
  }

  @override
  void dispose() {
    _selectedEvents.dispose();
    super.dispose();
  }

  void _fetchEventsForMonth(DateTime month) {
    _eventService.getEventsForMonth(month.year, month.month).then((events) {
      if (!mounted) return;
      setState(() {
        _monthlyEvents.clear();
        for (var event in events) {
          final day = DateTime.utc(event.startDate.year, event.startDate.month, event.startDate.day);
          (_monthlyEvents[day] ??= []).add(event);
        }
      });
    }).catchError((e) {
      // Handle error
    });
  }

  List<Event> _getEventsForDay(DateTime day) {
    return _monthlyEvents[DateTime.utc(day.year, day.month, day.day)] ?? [];
  }

  void _onDaySelected(DateTime selectedDay, DateTime focusedDay) {
    if (!isSameDay(_selectedDay, selectedDay)) {
      setState(() {
        _selectedDay = selectedDay;
        _focusedDay = focusedDay;
      });
      _selectedEvents.value = _getEventsForDay(selectedDay);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text("Calendário de Eventos", style: GoogleFonts.poppins(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          TableCalendar<Event>(
            locale: 'pt_BR',
            firstDay: DateTime.utc(2020, 1, 1),
            lastDay: DateTime.utc(2030, 12, 31),
            focusedDay: _focusedDay,
            selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
            eventLoader: _getEventsForDay,
            startingDayOfWeek: StartingDayOfWeek.monday,
            onDaySelected: _onDaySelected,
            onPageChanged: (focusedDay) {
              _focusedDay = focusedDay;
              _fetchEventsForMonth(focusedDay);
            },
            calendarStyle: const CalendarStyle(
              todayDecoration: BoxDecoration(color: Colors.grey, shape: BoxShape.circle),
              selectedDecoration: BoxDecoration(color: Color(0xFF00838A), shape: BoxShape.circle),
              markerDecoration: BoxDecoration(color: Color(0xFF98CE00), shape: BoxShape.circle),
            ),
            headerStyle: HeaderStyle(
              titleCentered: true,
              formatButtonVisible: false,
              titleTextStyle: GoogleFonts.poppins(fontWeight: FontWeight.bold, fontSize: 16),
            ),
          ),
          const SizedBox(height: 16),
          Text("Eventos do dia selecionado:", style: GoogleFonts.poppins(fontSize: 16)),
          Expanded(
            child: ValueListenableBuilder<List<Event>>(
              valueListenable: _selectedEvents,
              builder: (context, value, _) {
                if (value.isEmpty) {
                  return const Center(child: Text("Nenhum evento para este dia."));
                }
                return ListView.builder(
                  itemCount: value.length,
                  itemBuilder: (context, index) {
                    return ListTile(title: Text(value[index].title));
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
