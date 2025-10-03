
import 'package:flutter/material.dart';
import 'package:frontend/app/data/models/community.dart';
import 'package:frontend/app/data/services/community_service.dart';

class CommunityScreen extends StatefulWidget {
  const CommunityScreen({super.key});

  @override
  State<CommunityScreen> createState() => _CommunityScreenState();
}

class _CommunityScreenState extends State<CommunityScreen> {
  late Future<List<Community>> _futureCommunities;
  final CommunityService _communityService = CommunityService();

  @override
  void initState() {
    super.initState();
    _futureCommunities = _communityService.getCommunities();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Comunidades'),
        backgroundColor: const Color(0xFF003641),
      ),
      body: FutureBuilder<List<Community>>(
        future: _futureCommunities,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Erro ao carregar comunidades: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Nenhuma comunidade encontrada.'));
          } else {
            final communities = snapshot.data!;
            return ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: communities.length,
              itemBuilder: (context, index) {
                return _CommunityCard(community: communities[index]);
              },
            );
          }
        },
      ),
    );
  }
}

class _CommunityCard extends StatelessWidget {
  final Community community;

  const _CommunityCard({required this.community});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      margin: const EdgeInsets.only(bottom: 16.0),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              community.name,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF004B44)),
            ),
            const SizedBox(height: 8),
            Text(community.description, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(Icons.group, color: Colors.grey),
                    const SizedBox(width: 4),
                    Text('${community.memberCount} membros'),
                  ],
                ),
                Text(
                  community.communityType.toUpperCase(),
                  style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF93C83E)),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
