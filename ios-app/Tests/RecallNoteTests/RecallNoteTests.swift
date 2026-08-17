import XCTest
@testable import RecallNote

final class RecallNoteTests: XCTestCase {
    
    func testSpeakerDiarizationService() {
        let service = SpeakerDiarizationService()
        let dummyData = Data([0x00, 0x01, 0x02])
        
        let expectation = XCTestExpectation(description: "Process audio stream")
        
        service.processAudioStream(dummyData) { speaker in
            XCTAssertEqual(speaker.name, "Speaker 1")
            XCTAssertNotNil(speaker.voicePrint)
            XCTAssertEqual(speaker.voicePrint?.count, 3)
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 2.0)
    }
    
    func testTranscriptionService() {
        let service = TranscriptionService()
        let dummyURL = URL(fileURLWithPath: "/tmp/dummy.m4a")
        
        let expectation = XCTestExpectation(description: "Transcribe audio")
        
        service.transcribe(audioURL: dummyURL) { text in
            XCTAssertNotNil(text)
            XCTAssertTrue(text!.contains("Whisper model"))
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 3.0)
    }
    
    func testNoteModel() {
        let note = Note(textContent: "Test note")
        XCTAssertEqual(note.textContent, "Test note")
        XCTAssertNotNil(note.id)
    }
}
