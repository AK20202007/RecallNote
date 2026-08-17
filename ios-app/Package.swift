// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "RecallNote",
    platforms: [
        .iOS(.v15),
        .macOS(.v12)
    ],
    products: [
        .library(name: "RecallNote", targets: ["RecallNote"]),
    ],
    targets: [
        .target(
            name: "RecallNote",
            path: ".",
            exclude: ["Tests", "RecallNoteApp.swift", "Views/ContentView.swift"],
            sources: ["Models", "Services"]
        ),
        .testTarget(
            name: "RecallNoteTests",
            dependencies: ["RecallNote"],
            path: "Tests/RecallNoteTests"
        ),
    ]
)
