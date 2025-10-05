import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';

class EventDetailsPage extends StatelessWidget {
  final Event event;

  const EventDetailsPage({Key? key, required this.event}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF003641), // Dark theme background
      appBar: AppBar(
        title: const Text('Detalhes do Evento'),
        backgroundColor: const Color(0xFF004B44),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // --- Title ---
            Text(
              event.title,
              style: GoogleFonts.poppins(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 24),

            // --- Date & Time Info ---
            _buildInfoRow(Icons.calendar_today, 'Início', _formatDateTime(event.startDate)),
            if (event.endDate != null)
              _buildInfoRow(Icons.calendar_today_outlined, 'Fim', _formatDateTime(event.endDate!)),
            const SizedBox(height: 16),

            // --- Location Info ---
            _buildInfoRow(Icons.location_on, 'Local', event.location),
            if (event.address != null)
              _buildInfoRow(Icons.pin_drop, 'Endereço', event.address!),
            const SizedBox(height: 24),

            // --- Description ---
            Text(
              'Sobre o evento',
              style: GoogleFonts.poppins(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              event.description,
              style: GoogleFonts.lato(
                fontSize: 16,
                color: Colors.white.withOpacity(0.8),
                height: 1.5,
              ),
            ),
            const SizedBox(height: 32),

            // --- Register Button ---
            if (event.registrationsOpen)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    // TODO: Implement registration logic here, maybe show a confirmation dialog
                  },
                  icon: const Icon(Icons.check_circle_outline),
                  label: const Text('Realizar Inscrição'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF00838A),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    textStyle: GoogleFonts.poppins(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
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
                Text(
                  label,
                  style: GoogleFonts.poppins(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Colors.white70,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: GoogleFonts.lato(
                    fontSize: 16,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
