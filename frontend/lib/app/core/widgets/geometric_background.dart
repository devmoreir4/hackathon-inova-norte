import 'package:flutter/material.dart';

class GeometricBackground extends StatelessWidget {
  final Widget child;

  const GeometricBackground({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: _GeometricPainter(),
      child: child,
    );
  }
}

class _GeometricPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = const Color(0xFF04575c);
    canvas.drawPaint(paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
