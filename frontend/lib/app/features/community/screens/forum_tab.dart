import 'package:flutter/material.dart';
import 'package:frontend/app/data/models/post.dart';
import 'package:frontend/app/data/services/forum_service.dart';
import 'package:frontend/app/features/community/screens/create_post_screen.dart';
import 'package:frontend/app/features/community/widgets/post_card.dart';
import 'dart:collection';

class ForumTab extends StatefulWidget {
  const ForumTab({super.key});

  @override
  State<ForumTab> createState() => _ForumTabState();
}

class _ForumTabState extends State<ForumTab> {
  final ForumService _forumService = ForumService();
  List<Post> _allPosts = [];
  List<Post> _displayedPosts = [];
  List<String> _categories = [];
  String? _selectedCategory;
  bool _isLoading = true;

  final _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchPosts();
    _searchController.addListener(() {
      _applyFilters();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _fetchPosts() async {
    setState(() { _isLoading = true; });
    try {
      final posts = await _forumService.getPosts();
      if (!mounted) return;

      final categories = LinkedHashSet<String>.from(posts.map((p) => p.category)).toList();

      setState(() {
        _allPosts = posts;
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
    List<Post> filtered = _allPosts;

    // Filter by category
    if (_selectedCategory != null && _selectedCategory != 'Todos') {
      filtered = filtered.where((p) => p.category == _selectedCategory).toList();
    }

    // Filter by search query
    final query = _searchController.text.toLowerCase();
    if (query.isNotEmpty) {
      filtered = filtered.where((post) =>
              post.title.toLowerCase().contains(query) ||
              post.content.toLowerCase().contains(query))
          .toList();
    }

    setState(() {
      _displayedPosts = filtered;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildCategoryFilters(),
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 8), // Adjusted padding
          child: Row(
            children: [
              Expanded(
                flex: 2,
                child: TextField(
                  controller: _searchController,
                  style: const TextStyle(color: Colors.black),
                  decoration: InputDecoration(
                    hintText: 'Pesquisar no fórum...',
                    hintStyle: const TextStyle(color: Colors.grey),
                    filled: true,
                    fillColor: Colors.white,
                    prefixIcon: const Icon(Icons.search, color: Colors.grey),
                    suffixIcon: _searchController.text.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear, color: Colors.black),
                            onPressed: () => _searchController.clear(),
                          )
                        : null,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(30.0),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 16.0),
              Expanded(
                flex: 1,
                child: ElevatedButton.icon(
                  onPressed: () async {
                    final result = await Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const CreatePostScreen()),
                    );
                    if (result == true) {
                      _fetchPosts();
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF003C44),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30.0),
                    ),
                  ),
                  icon: const Icon(Icons.add, color: Colors.white),
                  label: const Text('Novo Post', style: TextStyle(color: Colors.white)),
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : RefreshIndicator(
                  onRefresh: _fetchPosts,
                  child: _displayedPosts.isEmpty
                      ? const Center(
                          child: Text(
                            'Nenhum post encontrado.',
                            style: TextStyle(color: Colors.white70),
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.only(top: 8),
                          itemCount: _displayedPosts.length,
                          itemBuilder: (context, index) {
                            return PostCard(post: _displayedPosts[index]);
                          },
                        ),
                ),
        ),
      ],
    );
  }

  Widget _buildCategoryFilters() {
    if (_categories.isEmpty) return const SizedBox.shrink();
    return SizedBox(
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
              label: Text(category),
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
    );
  }
}
