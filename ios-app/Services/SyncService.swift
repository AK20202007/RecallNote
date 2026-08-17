import Foundation

class SyncService {
    // Placeholder for syncing logic to Python FastAPI backend
    func syncNotes(_ notes: [Note], completion: @escaping (Bool) -> Void) {
        print("Syncing notes to backend...")
        
        let url = URL(string: "http://localhost:8000/sync/notes")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let data = try JSONEncoder().encode(notes)
            request.httpBody = data
            
            // Simulate network request
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
                print("Sync successful.")
                completion(true)
            }
        } catch {
            print("Failed to encode notes.")
            completion(false)
        }
    }
}
