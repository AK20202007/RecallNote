import SwiftUI

struct ContentView: View {
    @State private var notes: [Note] = []
    @State private var isRecording = false
    
    var body: some View {
        NavigationView {
            VStack {
                List(notes) { note in
                    VStack(alignment: .leading) {
                        Text(note.textContent)
                            .font(.body)
                        Text(note.createdAt, style: .date)
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                }
                
                Button(action: toggleRecording) {
                    Image(systemName: isRecording ? "stop.circle.fill" : "mic.circle.fill")
                        .resizable()
                        .frame(width: 64, height: 64)
                        .foregroundColor(isRecording ? .red : .blue)
                        .padding()
                }
            }
            .navigationTitle("Recall Notes")
        }
    }
    
    private func toggleRecording() {
        isRecording.toggle()
        // In a real app, this would trigger AudioRecorder and TranscriptionService
        if !isRecording {
            let newNote = Note(textContent: "This is a transcribed note from your on-device AI.", embedding: [0.1, 0.2, 0.3])
            notes.append(newNote)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
