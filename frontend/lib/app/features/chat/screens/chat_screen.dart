import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/data/services/rag_chat_service.dart';
import 'package:uuid/uuid.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final RagChatService _chatService = RagChatService();
  final List<Map<String, dynamic>> _messages = [];
  final ScrollController _scrollController = ScrollController();
  final String _sessionId = const Uuid().v4();
  bool _isLoading = false;

  final List<String> _suggestedQuestions = [
    'O que é cooperativismo?',
    'Quais os benefícios de ser um cooperado Sicoob?',
    'Como posso investir no Sicoob?',
    'Como posso iniciar minha educação financeira?',    'Onde encontro as agências Sicoob?',
  ];

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _sendMessage({String? text}) async {
    final messageText = text ?? _messageController.text.trim();
    if (messageText.isEmpty) return;

    setState(() {
      _messages.add({'text': messageText, 'isUser': true});
      _messages.add({'text': '', 'isUser': false, 'isTyping': true}); // Add typing indicator
      _isLoading = true;
    });
    _messageController.clear();
    _scrollToBottom();

    try {
      final response = await _chatService.sendMessage(messageText, _sessionId);
      setState(() {
        _messages.removeLast(); // Remove typing indicator
        _messages.add({'text': response['response'], 'isUser': false, 'sources': response['sources']});
      });
    } catch (e) {
      setState(() {
        _messages.removeLast(); // Remove typing indicator
        _messages.add({'text': 'Erro: ${e.toString()}', 'isUser': false});
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
      _scrollToBottom();
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sicoob IA'),
        backgroundColor: const Color(0xFF003C44),
        elevation: 0,
      ),
      body: Container(
        color: const Color(0xFF04575c), // Geometric background color
        child: Column(
          children: [
            Expanded(
              child: _messages.isEmpty && !_isLoading
                  ? _buildWelcomeSection()
                  : ListView.builder(
                      controller: _scrollController,
                      padding: const EdgeInsets.all(16.0),
                      itemCount: _messages.length,
                      itemBuilder: (context, index) {
                        final message = _messages[index];
                        return _ChatMessageBubble(
                          text: message['text'],
                          isUser: message['isUser'],
                          sources: message['sources'],
                          isTyping: message['isTyping'] ?? false,
                        );
                      },
                    ),
            ),
            _buildMessageInput(),
          ],
        ),
      ),
    );
  }

  Widget _buildWelcomeSection() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Image.asset(
              'assets/logo.png', // Assuming you have a logo for the AI or Sicoob
              height: 100,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 24),
          const Text(
            'Olá! Eu sou o seu assistente virtual do Sicoob.',
            style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          const Text(
            'Posso te ajudar com informações sobre cooperativismo, produtos e serviços do Sicoob, educação financeira e muito mais. Digite sua pergunta ou escolha uma das sugestões abaixo.',
            style: TextStyle(color: Colors.white70, fontSize: 16),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 32),
          const Text(
            'Perguntas Sugeridas:',
            style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8.0, // gap between adjacent chips
            runSpacing: 8.0, // gap between lines
            children: _suggestedQuestions.map((question) {
              return ActionChip(
                onPressed: () => _sendMessage(text: question),
                label: Text(question),
                labelStyle: const TextStyle(color: Colors.white, fontSize: 14),
                backgroundColor: const Color(0xFF004B44), // Sicoob primaryDark
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20.0),
                  side: BorderSide(color: Colors.white.withOpacity(0.5)),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageInput() {
    return Container(
      padding: const EdgeInsets.all(8.0),
      decoration: BoxDecoration(
        color: const Color(0xFF003C44), // Darker teal for input area
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            spreadRadius: 1,
            blurRadius: 5,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _messageController,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: 'Digite sua mensagem...',
                hintStyle: TextStyle(color: Colors.white.withOpacity(0.7)),
                filled: true,
                fillColor: const Color(0xFF004B44), // Slightly lighter teal for text field
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(25.0),
                  borderSide: BorderSide.none,
                ),
                contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              ),
              onSubmitted: (_) => _sendMessage(),
            ),
          ),
          const SizedBox(width: 8.0),
          FloatingActionButton(
            onPressed: () => _sendMessage(),
            backgroundColor: const Color(0xFF00838A), // Sicoob primaryMedium color
            mini: true,
            elevation: 2,
            child: const Icon(Icons.send, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class _ChatMessageBubble extends StatelessWidget {
  final String text;
  final bool isUser;
  final List<dynamic>? sources;
  final bool isTyping;

  const _ChatMessageBubble({required this.text, required this.isUser, this.sources, this.isTyping = false});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4.0, horizontal: 8.0),
        padding: const EdgeInsets.all(12.0),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
        decoration: BoxDecoration(
          color: isUser ? const Color(0xFF00838A) : const Color(0xFF004B44), // Sicoob colors
          borderRadius: BorderRadius.circular(12.0),
        ),
        child: Column(
          crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          children: [
            if (!isUser && !isTyping) // Only show avatar for AI messages that are not typing indicators
              Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: CircleAvatar(
                  backgroundColor: Colors.white,
                  radius: 16,
                  child: Image.asset(
                    'assets/icon.png', // Use a specific icon for the AI
                    height: 24,
                    width: 24,
                  ),
                ),
              ),
            isTyping
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      color: Colors.white,
                      strokeWidth: 2,
                    ),
                  )
                : MarkdownBody(
                    data: text,
                    styleSheet: MarkdownStyleSheet.fromTheme(
                      Theme.of(context).copyWith(
                        textTheme: Theme.of(context).textTheme.apply(
                              bodyColor: Colors.white,
                              displayColor: Colors.white,
                            ),
                      ),
                    ).copyWith(
                      p: const TextStyle(color: Colors.white, fontSize: 15.0),
                      strong: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 15.0),
                      em: const TextStyle(fontStyle: FontStyle.italic, color: Colors.white, fontSize: 15.0),
                      listBullet: const TextStyle(color: Colors.white, fontSize: 15.0),
                      h1: const TextStyle(color: Colors.white, fontSize: 24.0, fontWeight: FontWeight.bold),
                      h2: const TextStyle(color: Colors.white, fontSize: 22.0, fontWeight: FontWeight.bold),
                      h3: const TextStyle(color: Colors.white, fontSize: 20.0, fontWeight: FontWeight.bold),
                      h4: const TextStyle(color: Colors.white, fontSize: 18.0, fontWeight: FontWeight.bold),
                      h5: const TextStyle(color: Colors.white, fontSize: 16.0, fontWeight: FontWeight.bold),
                      h6: const TextStyle(color: Colors.white, fontSize: 15.0, fontWeight: FontWeight.bold),
                    ),
                    selectable: true,
                  ),
            if (!isTyping && sources != null && sources!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text(
                  'Fontes: ${sources!.join(', ')}',
                  style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 10.0),
                  textAlign: isUser ? TextAlign.right : TextAlign.left,
                ),
              ),
          ],
        ),
      ),
    );
  }
}