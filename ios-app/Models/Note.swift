import Foundation

struct Speaker: Identifiable, Codable {
    var id: UUID = UUID()
    var name: String
    var voicePrint: [Float]? // Abstract representation of voice biometrics
}

struct Note: Identifiable, Codable {
    var id: UUID = UUID()
    var textContent: String
    var speakerId: UUID?
    var embedding: [Float]?
    var createdAt: Date = Date()
    var updatedAt: Date = Date()
}
