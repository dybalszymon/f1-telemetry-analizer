from presentation.ReportRenderer import ReportRenderer


class CliRenderer(ReportRenderer):
    def render(self, title: str, data):
        """Renderuje dane w CLI z lepszym formatowaniem"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60)
        
        if isinstance(data, dict):
            # Obsługa FastestLapStrategy
            if 'driver' in data and 'time' in data:
                print(f"  Kierowca: #{data['driver']}")
                print(f"  Czas: {data['time']:.3f}s")
                if 'lap_number' in data:
                    print(f"  Okrążenie: {data['lap_number']}")
            
            # Obsługa ConsistencyScoreStrategy
            elif 'consistency_score' in data:
                print(f"  Kierowca: #{data['driver']}")
                print(f"  Średni czas: {data['avg_time']:.3f}s")
                print(f"  Odchylenie: {data['std_dev']:.3f}s")
                print(f"  Wynik konsystencji: {data['consistency_score']:.1f}")
                print(f"  Okrążeń: {data['laps_count']}")
            
            else:
                for key, value in data.items():
                    print(f"  {key}: {value}")
        
        elif isinstance(data, list):
            # Obsługa list wykresów z TelemetryComposite
            print(f"  Wygenerowano {len(data)} wykresów telemetrii")
            for i, plot in enumerate(data, 1):
                if isinstance(plot, dict) and 'label' in plot:
                    drivers = plot.get('drivers', {})
                    print(f"  {i}. {plot['label']} - {len(drivers)} kierowców")
        else:
            print(f"  Wynik: {data}")
        
        print("="*60 + "\n")
