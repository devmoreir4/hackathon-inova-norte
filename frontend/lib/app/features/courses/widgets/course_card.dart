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
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      elevation: 5,
      shadowColor: Colors.black.withOpacity(0.1),
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
                    height: 180,
                    fit: BoxFit.cover,
                    // Loading and error builders can be added for better UX
                    loadingBuilder: (context, child, progress) {
                      return progress == null
                          ? child
                          : const SizedBox(
                              height: 180,
                              child: Center(child: CircularProgressIndicator()),
                            );
                    },
                    errorBuilder: (context, error, stackTrace) {
                      return const SizedBox(
                        height: 180,
                        child: Icon(Icons.school, size: 50, color: Colors.grey),
                      );
                    },
                  )
                : const SizedBox(
                    height: 180,
                    child: Icon(Icons.school, size: 50, color: Colors.grey),
                  ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  course.title,
                  style: GoogleFonts.poppins(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: const Color(0xFF003C44), // Sicoob dark green
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  course.description,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: GoogleFonts.lato(
                    fontSize: 14,
                    color: Colors.black54,
                  ),
                ),
                const SizedBox(height: 16),
                Align(
                  alignment: Alignment.center,
                  child: ElevatedButton(
                    onPressed: () {
                      // TODO: Implement navigation to course details screen
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF98CE00), // Sicoob green
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 12),
                    ),
                    child: Text(
                      'Quero aprender',
                      style: GoogleFonts.poppins(
                        fontWeight: FontWeight.bold,
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
