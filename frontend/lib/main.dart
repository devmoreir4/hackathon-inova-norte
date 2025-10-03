import 'package:flutter/material.dart';
import 'package:frontend/app/core/theme/theme.dart';
import 'package:frontend/app/features/auth/screens/login_screen.dart';

void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Sicoob',
      theme: AppTheme.theme,
      home: const LoginScreen(),
    );
  }
}
