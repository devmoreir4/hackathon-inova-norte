import 'package:flutter/material.dart';
import 'package:frontend/app/features/courses/models/course.dart';
import 'package:google_fonts/google_fonts.dart';

class CourseCard extends StatelessWidget {
  final Course course;

  const CourseCard({Key? key, required this.course}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    String? imageUrl = course.imageUrl;
    // Temporary fix: If the image URL is a placeholder from example.com, replace it.
    if (imageUrl != null && imageUrl.contains('example.com')) {
      // Use a placeholder service like picsum.photos with the course ID for a unique image
      imageUrl = 'https://picsum.photos/seed/${course.id}/400/200';
    }

    return Card(
      color: Colors.white, // Force card background to be white
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      elevation: 4,
      shadowColor: Colors.black.withOpacity(0.2),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          ClipRRect(
            borderRadius: const BorderRadius.only(
              topLeft: Radius.circular(16),
              topRight: Radius.circular(16),
            ),
            child: imageUrl != null
                ? Image.network(
                    imageUrl,
                    height: 160,
                    fit: BoxFit.cover,
                    loadingBuilder: (context, child, progress) {
                      return progress == null
                          ? child
                          : const SizedBox(
                              height: 160,
                              child: Center(child: CircularProgressIndicator()),
                            );
                    },
                    errorBuilder: (context, error, stackTrace) {
                      return Container(
                        height: 160,
                        color: Colors.grey[200],
                        child: Icon(Icons.school_outlined, size: 50, color: Colors.grey[400]),
                      );
                    },
                  )
                : Container(
                    height: 160,
                    color: Colors.grey[200],
                    child: Icon(Icons.school_outlined, size: 50, color: Colors.grey[400]),
                  ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  course.title,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: GoogleFonts.poppins(
                    fontSize: 17,
                    fontWeight: FontWeight.w600, // Bolder for more emphasis
                    color: const Color(0xFF003C44), // Sicoob dark green
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  course.description,
                  maxLines: 3, // Allow more text for description
                  overflow: TextOverflow.ellipsis,
                  style: GoogleFonts.lato(
                    fontSize: 14,
                    color: Colors.black.withOpacity(0.6),
                    height: 1.4, // Improved line spacing
                  ),
                ),
                const SizedBox(height: 20),
                Center(
                  child: ElevatedButton(
                    onPressed: () {
                      // TODO: Implement navigation to course details screen
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF98CE00), // Sicoob green
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(25),
                      ),
                      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                      elevation: 2,
                    ),
                    child: Text(
                      'Quero aprender',
                      style: GoogleFonts.poppins(
                        fontWeight: FontWeight.bold,
                        fontSize: 15,
                        color: Colors.white,
                      ),
                    ),
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
