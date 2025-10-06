import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/services/event_service.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';

class EventDetailsPage extends StatefulWidget {
  final Event event;

  const EventDetailsPage({Key? key, required this.event}) : super(key: key);

  @override
  _EventDetailsPageState createState() => _EventDetailsPageState();
}

class _EventDetailsPageState extends State<EventDetailsPage> {
  final EventService _eventService = EventService();
  bool? _isRegistered;
  int? _registrationId;

  @override
  void initState() {
    super.initState();
    _checkRegistrationStatus();
  }

  Future<void> _checkRegistrationStatus() async {
    const userId = 1; // Placeholder
    try {
      final registrations = await _eventService.getRegistrationsForUser(userId);
      
      dynamic registration; // Use dynamic to handle potential null
      try {
        registration = registrations.firstWhere((reg) => reg.eventId == widget.event.id);
      } catch (e) {
        registration = null;
      }

      if (mounted) {
        setState(() {
          _isRegistered = registration != null;
          _registrationId = registration?.id;
        });
      }
    } catch (e) {
      // Handle error fetching registrations
    }
  }

  void _toggleRegistration(BuildContext context) {
    const userId = 1; // Placeholder

    if (_isRegistered == true && _registrationId != null) {
      // Unregister
      _eventService.unregisterFromEvent(widget.event.id, _registrationId!).then((_) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Inscrição cancelada.'), backgroundColor: Colors.orange));
        if (mounted) setState(() { _isRegistered = false; _registrationId = null; });
      }).catchError((e) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro ao cancelar: $e'), backgroundColor: Colors.red));
      });
    } else {
      // Register
      _eventService.registerForEvent(widget.event.id, userId).then((_) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Inscrição realizada com sucesso!'), backgroundColor: Colors.green));
        // Re-check status to get the new registration ID
        _checkRegistrationStatus();
      }).catchError((e) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro na inscrição: $e'), backgroundColor: Colors.red));
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF003641),
      appBar: AppBar(
        title: const Text('Detalhes do Evento'),
        backgroundColor: const Color(0xFF004B44),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.event.title, style: GoogleFonts.poppins(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 24),
            _buildInfoRow(Icons.calendar_today, 'Início', _formatDateTime(widget.event.startDate)),
            if (widget.event.endDate != null) _buildInfoRow(Icons.calendar_today_outlined, 'Fim', _formatDateTime(widget.event.endDate!)),
            const SizedBox(height: 16),
            _buildInfoRow(Icons.location_on, 'Local', widget.event.location),
            if (widget.event.address != null) _buildInfoRow(Icons.pin_drop, 'Endereço', widget.event.address!),
            const SizedBox(height: 24),
            Text('Sobre o evento', style: GoogleFonts.poppins(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 8),
            Text(widget.event.description, style: GoogleFonts.lato(fontSize: 16, color: Colors.white.withOpacity(0.8), height: 1.5)),
            const SizedBox(height: 32),
            _buildRegistrationButton(),
          ],
        ),
      ),
    );
  }

  Widget _buildRegistrationButton() {
    if (_isRegistered == null) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_isRegistered!) {
      return SizedBox(
        width: double.infinity,
        child: ElevatedButton.icon(
          onPressed: () => _toggleRegistration(context),
          icon: const Icon(Icons.cancel_outlined),
          label: const Text('Cancelar Inscrição'),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.red.shade700,
            padding: const EdgeInsets.symmetric(vertical: 16),
            textStyle: GoogleFonts.poppins(fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ),
      );
    } else {
      if (widget.event.registrationsOpen) {
        return SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () => _toggleRegistration(context),
            icon: const Icon(Icons.check_circle_outline),
            label: const Text('Realizar Inscrição'),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF00838A),
              padding: const EdgeInsets.symmetric(vertical: 16),
              textStyle: GoogleFonts.poppins(fontSize: 16, fontWeight: FontWeight.bold),
            ),
          ),
        );
      } else {
        return const SizedBox.shrink(); // Or a disabled button
      }
    }
  }

  String _formatDateTime(DateTime dateTime) {
    return DateFormat("dd/MM/yyyy 'às' HH:mm", 'pt_BR').format(dateTime);
  }

  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Colors.white70, size: 20),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: GoogleFonts.poppins(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.white70)),
                const SizedBox(height: 2),
                Text(value, style: GoogleFonts.lato(fontSize: 16, color: Colors.white)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
