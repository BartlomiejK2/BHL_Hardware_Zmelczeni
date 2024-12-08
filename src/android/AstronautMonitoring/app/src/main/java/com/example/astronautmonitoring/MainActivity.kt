package com.example.astronautmonitoring

import android.graphics.Color
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import android.widget.Toast
import androidx.core.graphics.ColorUtils

class MainActivity : AppCompatActivity() {

    private lateinit var astronautRecyclerView: RecyclerView
    private lateinit var astronautAdapter: AstronautAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        astronautRecyclerView = findViewById(R.id.recyclerView)
        astronautRecyclerView.layoutManager = LinearLayoutManager(this)

        // Sample list of astronauts, with unique colors for profile pictures
        val astronauts = listOf(
            Astronaut("Astronaut 1", "Healthy", "Happy", R.drawable.kotek_1),
            Astronaut("Astronaut 2", "Critical", "Stressed", R.drawable.kotek_2),
            Astronaut("Astronaut 3", "Stable", "Neutral", R.drawable.kotek_3)
        )

        astronautAdapter = AstronautAdapter(astronauts) { astronaut ->
            onAstronautSelected(astronaut)
        }

        astronautRecyclerView.adapter = astronautAdapter
    }

    private fun onAstronautSelected(astronaut: Astronaut) {
        Toast.makeText(this, "Viewing video feed for ${astronaut.name}", Toast.LENGTH_SHORT).show()
        // Here you would integrate video feed logic, but we mock it for now
    }

    // Function to generate a color for the astronaut's profile picture
    private fun generateProfileColor(name: String): Int {
        // Generate a color based on the astronaut's name (using hash code, for example)
        val colorCode = name.hashCode() // Generate a unique hash code
        return Color.argb(255, (colorCode shr 16) and 0xFF, (colorCode shr 8) and 0xFF, colorCode and 0xFF)
    }
}
