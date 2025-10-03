
import 'package:flutter/material.dart';
import 'dart:ui';

class GeometricBackground extends StatelessWidget {
  const GeometricBackground({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: _GeometricPainter(),
      child: Container(),
    );
  }
}

class _GeometricPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paintLimeGreen = Paint()..color = const Color(0xFF93C83E);
    final paintBrightGreen = Paint()..color = const Color(0xFF66B23E);
    final paintMediumTeal = Paint()..color = const Color(0xFF00838A);
    final paintDarkTeal = Paint()..color = const Color(0xFF004B44);

    // Final paths based on the user's provided image 1.jpg
    
    // Dark Teal background shape
    final pathDarkTeal = Path()
      ..moveTo(size.width * 0.4, 0)
      ..lineTo(size.width, 0)
      ..lineTo(size.width, size.height * 0.8)
      ..lineTo(size.width * 0.7, size.height)
      ..close();
    canvas.drawPath(pathDarkTeal, paintDarkTeal);

    // Medium Teal top-right shape
    final pathMediumTeal = Path()
      ..moveTo(size.width * 0.5, 0)
      ..lineTo(size.width, 0)
      ..lineTo(size.width, size.height * 0.4)
      ..close();
    canvas.drawPath(pathMediumTeal, paintMediumTeal);

    // Bright Green main shape
    final pathBrightGreen = Path()
      ..moveTo(0, 0)
      ..lineTo(size.width * 0.85, 0)
      ..lineTo(0, size.height * 0.8)
      ..close();
    canvas.drawPath(pathBrightGreen, paintBrightGreen);

    // Lime Green accent shape
    final pathLimeGreen = Path()
      ..moveTo(0, size.height * 0.9)
      ..lineTo(size.width * 0.5, size.height * 0.2)
      ..lineTo(size.width * 0.3, size.height)
      ..lineTo(0, size.height)
      ..close();
    canvas.drawPath(pathLimeGreen, paintLimeGreen);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
