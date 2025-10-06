import 'package:flutter/material.dart';
import 'package:frontend/app/core/theme/theme.dart';
import 'package:frontend/app/features/auth/screens/login_screen.dart';
import 'package:frontend/app/features/home/screens/home_screen.dart'; // Adicionar este import
import 'package:intl/date_symbol_data_local.dart';

void main() async {
  // Ensure flutter bindings are initialized
  WidgetsFlutterBinding.ensureInitialized();
  // Initialize locale data for date formatting
  await initializeDateFormatting('pt_BR', null);
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
      home: const HomeScreen(), // Mudar para HomeScreen()
    );
  }
}
