import SwiftUI

struct AnalyzerView: View {
    @State private var amount: String = ""
    @State private var modelProbability: String = ""
    @State private var countryCode: String = ""
    @State private var velocity: String = "Normal"
    @State private var result: String = "Run analysis to get decision output."

    private let levels = ["Normal", "High", "Extreme"]

    var body: some View {
        NavigationStack {
            Form {
                Section("Input") {
                    TextField("Amount (EUR)", text: $amount)
                        .keyboardType(.decimalPad)
                    TextField("Model Probability (%)", text: $modelProbability)
                        .keyboardType(.decimalPad)
                    TextField("Country Code (e.g., RU)", text: $countryCode)
                        .textInputAutocapitalization(.characters)
                    Picker("Velocity", selection: $velocity) {
                        ForEach(levels, id: \.self) { level in
                            Text(level)
                        }
                    }
                }

                Section("Actions") {
                    Button("Analyze") {
                        analyze()
                    }
                    Button("Load Sample") {
                        amount = "9200"
                        modelProbability = "61.5"
                        countryCode = "RU"
                        velocity = "High"
                        analyze()
                    }
                }

                Section("Result") {
                    Text(result)
                        .font(.system(.body, design: .monospaced))
                }
            }
            .navigationTitle("Data Analyzer iOS")
        }
    }

    private func analyze() {
        guard let amountValue = Double(amount),
              let probabilityPct = Double(modelProbability),
              !countryCode.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
        else {
            result = "Invalid input. Fill amount, probability, and country code."
            return
        }

        let country = countryCode.uppercased()
        var risk = probabilityPct / 100.0

        if amountValue > 10000 {
            risk *= 1.30
        } else if amountValue > 5000 {
            risk *= 1.15
        }

        if ["RU", "CN", "NG", "VE"].contains(country) {
            risk *= 1.25
        }

        if velocity == "High" {
            risk *= 1.20
        } else if velocity == "Extreme" {
            risk *= 1.40
        }

        risk = min(risk, 1.0)
        let decision = risk >= 0.65 ? "BLOCK / REVIEW" : "APPROVE"

        result = """
        Amount: EUR \(String(format: "%.2f", amountValue))
        Country: \(country)
        Velocity: \(velocity)
        Risk: \(String(format: "%.2f", risk * 100))%
        Decision: \(decision)
        """
    }
}
