import 'dart:collection';
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
  final CourseService _courseService = CourseService();
  List<Course> _allCourses = [];
  List<Course> _displayedCourses = [];
  List<String> _categories = [];
  String? _selectedCategory;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchCourses();
  }

  Future<void> _fetchCourses() async {
    setState(() { _isLoading = true; });
    try {
      final courses = await _courseService.fetchCourses();
      if (!mounted) return;

      final categories = LinkedHashSet<String>.from(courses.map((c) => c.category)).toList();

      setState(() {
        _allCourses = courses;
        _categories = ['Todos', ...categories];
        _selectedCategory = 'Todos';
        _applyFilters();
        _isLoading = false;
      });
    } catch (e) {
      setState(() { _isLoading = false; });
      // Handle error
    }
  }

  void _selectCategory(String category) {
    setState(() {
      _selectedCategory = category;
      _applyFilters();
    });
  }

  void _applyFilters() {
    List<Course> filtered = _allCourses;

    if (_selectedCategory != null && _selectedCategory != 'Todos') {
      filtered = filtered.where((c) => c.category == _selectedCategory).toList();
    }

    setState(() {
      _displayedCourses = filtered;
    });
  }

  Future<void> _refreshCourses() async {
    await _fetchCourses();
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
    return Column(
      children: [
        _buildCategoryFilters(),
        Expanded(
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : RefreshIndicator(
                  onRefresh: _refreshCourses,
                  child: _displayedCourses.isEmpty
                      ? const Center(
                          child: Text(
                            'Nenhum curso encontrado.',
                            style: TextStyle(color: Colors.white70),
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.only(top: 8),
                          itemCount: _displayedCourses.length,
                          itemBuilder: (context, index) {
                            return CourseCard(course: _displayedCourses[index]);
                          },
                        ),
                ),
        ),
      ],
    );
  }

  Widget _buildCategoryFilters() {
    if (_categories.isEmpty) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(top: 16.0, bottom: 8.0),
      child: SizedBox(
        height: 50,
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 12),
          itemCount: _categories.length,
          itemBuilder: (context, index) {
            final category = _categories[index];
            final isSelected = category == _selectedCategory;
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4.0),
              child: FilterChip(
                label: Text(_formatCategoryName(category)),
                selected: isSelected,
                onSelected: (selected) => _selectCategory(category),
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
