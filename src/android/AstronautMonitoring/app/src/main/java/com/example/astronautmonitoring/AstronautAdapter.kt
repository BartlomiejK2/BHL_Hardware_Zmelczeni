package com.example.astronautmonitoring

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import android.widget.ToggleButton
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.imageview.ShapeableImageView

class AstronautAdapter(
    private val astronauts: List<Astronaut>,
    private val onItemClicked: (Astronaut) -> Unit
) : RecyclerView.Adapter<AstronautAdapter.AstronautViewHolder>() {

    private var selectedPosition = -1  // Variable to keep track of the selected item

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AstronautViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_astronaut, parent, false)
        return AstronautViewHolder(view)
    }

    override fun onBindViewHolder(holder: AstronautViewHolder, position: Int) {
        val astronaut = astronauts[position]
        holder.bind(astronaut, onItemClicked, position)
    }

    override fun getItemCount() = astronauts.size

    inner class AstronautViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val profileImageView: ShapeableImageView = itemView.findViewById(R.id.profileImageView)
        private val nameTextView: TextView = itemView.findViewById(R.id.nameTextView)
        private val vitalsTextView: TextView = itemView.findViewById(R.id.vitalsTextView)
        private val emotionalStateTextView: TextView = itemView.findViewById(R.id.emotionalStateTextView)
        private val videoFeedToggleButton: ToggleButton = itemView.findViewById(R.id.videoFeedToggleButton)

        fun bind(astronaut: Astronaut, onItemClicked: (Astronaut) -> Unit, position: Int) {
            nameTextView.text = astronaut.name
            vitalsTextView.text = "Vitals: ${astronaut.vitals}"
            emotionalStateTextView.text = "Emotional State: ${astronaut.emotionalState}"

            // Set the profile image using the resource ID
            profileImageView.setImageResource(astronaut.profileImageResId)

            // Set the ToggleButton state
            videoFeedToggleButton.isChecked = position == selectedPosition

            // ToggleButton logic to ensure only one button can be on at a time
            videoFeedToggleButton.setOnCheckedChangeListener { _, isChecked ->
                if (isChecked) {
                    selectedPosition = position
                    notifyDataSetChanged()  // Notify adapter to update the button states
                } else if (selectedPosition == position) {
                    selectedPosition = -1  // Reset if the currently selected button is turned off
                    notifyDataSetChanged()
                }
            }

            itemView.setOnClickListener {
                onItemClicked(astronaut)
            }
        }
    }
}
