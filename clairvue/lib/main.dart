import 'package:flutter/material.dart';
import 'homepage.dart';

void main() {
  runApp(ColorBlindApp());
}

class ColorBlindApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Color Blind Correction',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: HomePage(),
    );
  }
}
