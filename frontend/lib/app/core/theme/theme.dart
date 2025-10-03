
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static const Color primaryDark = Color(0xFF004B44);
  static const Color primaryMedium = Color(0xFF00838A);
  static const Color accentGreen = Color(0xFF93C83E);
  static const Color backgroundDark = Color(0xFF003641);
  static const Color textWhite = Colors.white;

  static ThemeData get theme {
    return ThemeData(
      primaryColor: primaryDark,
      scaffoldBackgroundColor: backgroundDark,
      colorScheme: const ColorScheme.dark(
        primary: primaryDark,
        secondary: accentGreen,
        background: backgroundDark,
        onPrimary: textWhite,
        onSecondary: textWhite,
        onBackground: textWhite,
      ),
      textTheme: GoogleFonts.poppinsTextTheme(
        const TextTheme(
          headlineSmall: TextStyle(
            color: textWhite,
            fontWeight: FontWeight.bold,
            fontSize: 24,
          ),
          bodyLarge: TextStyle(
            color: textWhite,
            fontSize: 16,
          ),
          labelLarge: TextStyle(
            color: textWhite,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryDark,
          foregroundColor: textWhite,
          minimumSize: const Size(double.infinity, 56),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: GoogleFonts.poppins(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          backgroundColor: textWhite,
          foregroundColor: primaryDark,
          minimumSize: const Size(double.infinity, 56),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: GoogleFonts.poppins(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
    );
  }
}
