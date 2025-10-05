import 'package:flutter/material.dart';
import 'package:frontend/app/features/events/models/event.dart';
import 'package:frontend/app/features/events/screens/event_details_screen.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';

class EventCard extends StatelessWidget {
  final Event event;
  final bool isRegistered;

  const EventCard({Key? key, required this.event, required this.isRegistered}) : super(key: key);

  String _formatEventType(String eventType) {
    switch (eventType) {
      case 'cooperative_fair':
        return 'Feira Cooperativa';
      case 'lecture':
        return 'Palestra';
      case 'business_round':
        return 'Rodada de Negócios';
      case 'educational_activity':
        return 'Atividade Educativa';
      default:
        return 'Outro';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      color: Colors.white,
      elevation: 3,
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => EventDetailsPage(event: event),
            ),
          );
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(12),
                    topRight: Radius.circular(12),
                  ),
                  child: Image.network(
                    // Using picsum as a placeholder for event images
                    'https://picsum.photos/seed/${event.id}/400/200',
                    height: 120,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                       return Container(
                        height: 120,
                        color: Colors.grey[200],
                        child: Icon(Icons.event, size: 40, color: Colors.grey[400]),
                      );
                    },
                  ),
                ),
                Positioned(
                  top: 8,
                  left: 8,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
                    decoration: BoxDecoration(
                      color: isRegistered ? Colors.blue.shade600 : (event.registrationsOpen ? Colors.green.shade600 : Colors.red.shade600),
                      borderRadius: BorderRadius.circular(12.0),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(isRegistered ? Icons.star : (event.registrationsOpen ? Icons.check_circle_outline : Icons.cancel_outlined), color: Colors.white, size: 14),
                        const SizedBox(width: 4),
                        Text(
                          isRegistered ? 'Inscrito' : (event.registrationsOpen ? 'Aberto' : 'Fechado'),
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 10),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: IntrinsicHeight(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.stretch, // Stretch children to equal height
                  children: [
                    Container(
                      width: 85, // Increased width for better proportion
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: const Color(0xFF003C44).withOpacity(0.1),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            DateFormat('dd').format(event.startDate),
                            style: GoogleFonts.poppins(
                              color: const Color(0xFF003C44),
                              fontWeight: FontWeight.bold,
                              fontSize: 26, // Increased font size
                            ),
                          ),
                          Text(
                            DateFormat('MMM', 'pt_BR').format(event.startDate).toUpperCase(),
                            style: GoogleFonts.poppins(
                              color: const Color(0xFF003C44),
                              fontWeight: FontWeight.w600,
                              fontSize: 16, // Increased font size
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _formatEventType(event.eventType),
                            style: GoogleFonts.poppins(
                              fontWeight: FontWeight.w600,
                              fontSize: 11,
                              color: const Color(0xFF00838A),
                            ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            event.title,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: GoogleFonts.poppins(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                              color: const Color(0xFF003C44),
                            ),
                          ),
                          const Spacer(), // Pushes content below to the bottom
                          Row(
                            children: [
                              const Icon(Icons.access_time, size: 14, color: Colors.grey),
                              const SizedBox(width: 4),
                              Text(
                                DateFormat('HH:mm').format(event.startDate),
                                style: GoogleFonts.lato(color: Colors.grey[700]),
                              ),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Row(
                            children: [
                              const Icon(Icons.location_on_outlined, size: 14, color: Colors.grey),
                              const SizedBox(width: 4),
                              Flexible(
                                child: Text(
                                  event.location,
                                  overflow: TextOverflow.ellipsis,
                                  style: GoogleFonts.lato(color: Colors.grey[700]),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    const Center(
                      child: Icon(Icons.chevron_right, color: Colors.grey, size: 28),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
