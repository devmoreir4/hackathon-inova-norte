import 'package:flutter/material.dart';
import 'package:frontend/app/features/courses/models/course.dart';
import 'package:frontend/app/features/courses/services/course_service.dart';
import 'package:frontend/app/features/courses/widgets/course_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'dart:collection';

class CursosTab extends StatefulWidget {
  const CursosTab({Key? key}) : super(key: key);

  @override
  _CursosTabState createState() => _CursosTabState();
}

class _CursosTabState extends State<CursosTab> {
  final CourseService _courseService = CourseService();
  List<Course> _allCourses = [];
  List<Course> _filteredCourses = [];
  List<String> _categories = [];
  String? _selectedCategory;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });
    try {
      final courses = await _courseService.fetchCourses();
      final categories = LinkedHashSet<String>.from(courses.map((c) => c.category)).toList();
      setState(() {
        _allCourses = courses;
        _filteredCourses = courses;
        _categories = ['Todos', ...categories];
        _selectedCategory = 'Todos';
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  void _filterCourses(String category) {
    setState(() {
      _selectedCategory = category;
      if (category == 'Todos') {
        _filteredCourses = _allCourses;
      } else {
        _filteredCourses = _allCourses.where((c) => c.category == category).toList();
      }
    });
  }

  String _formatCategoryName(String category) {
    switch (category.toLowerCase()) {
      case 'financial_education':
        return 'Educação Financeira';
      case 'cooperativism':
        return 'Cooperativismo';
      case 'business':
        return 'Negócios';
      case 'todos':
        return 'Todos';
      default:
        return category; // Fallback for other categories
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            'Erro ao carregar os cursos.\nPor favor, tente novamente mais tarde.',
            textAlign: TextAlign.center,
            style: GoogleFonts.lato(color: Colors.white),
          ),
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _fetchData,
      child: Column(
        children: [
          _buildCategoryFilters(),
          Expanded(
            child: _filteredCourses.isEmpty
                ? Center(
                    child: Text(
                      'Nenhum curso encontrado para esta categoria.',
                      style: GoogleFonts.lato(color: Colors.white),
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.only(top: 8.0, bottom: 8.0),
                    itemCount: _filteredCourses.length,
                    itemBuilder: (context, index) {
                      return CourseCard(course: _filteredCourses[index]);
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryFilters() {
    return SizedBox(
      height: 60,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        itemCount: _categories.length,
        itemBuilder: (context, index) {
          final category = _categories[index];
          final isSelected = category == _selectedCategory;
          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4.0),
            child: FilterChip(
              label: Text(_formatCategoryName(category)),
              selected: isSelected,
              onSelected: (selected) => _filterCourses(category),
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
