import 'package:flutter/material.dart';
import 'package:frontend/app/features/courses/models/course.dart';
import 'package:frontend/app/features/courses/services/course_service.dart';
import 'package:frontend/app/features/courses/widgets/course_card.dart';
import 'package:google_fonts/google_fonts.dart';

class CursosTab extends StatefulWidget {
  const CursosTab({Key? key}) : super(key: key);

  @override
  _CursosTabState createState() => _CursosTabState();
}

class _CursosTabState extends State<CursosTab> {
  late Future<List<Course>> _coursesFuture;
  final CourseService _courseService = CourseService();

  @override
  void initState() {
    super.initState();
    _coursesFuture = _courseService.fetchCourses();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Course>>(
      future: _coursesFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(
                'Erro ao carregar os cursos.\nPor favor, tente novamente mais tarde.',
                textAlign: TextAlign.center,
                style: GoogleFonts.lato(),
              ),
            ),
          );
        }
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(
            child: Text(
              'Nenhum curso disponível no momento.',
              style: GoogleFonts.lato(),
            ),
          );
        }

        final courses = snapshot.data!;
        return ListView.builder(
          padding: const EdgeInsets.only(top: 8.0),
          itemCount: courses.length,
          itemBuilder: (context, index) {
            return CourseCard(course: courses[index]);
          },
        );
      },
    );
  }
}
