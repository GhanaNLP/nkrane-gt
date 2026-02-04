# nkrane/cli.py (optional command-line interface)
import argparse
import json
from .translator import NkraneTranslator
from .utils import list_available_options, export_terminology, save_sample_terminology

def main():
    parser = argparse.ArgumentParser(description="Nkrane - Enhanced Machine Translation")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Translate command
    translate_parser = subparsers.add_parser("translate", help="Translate text")
    translate_parser.add_argument("text", help="Text to translate")
    translate_parser.add_argument("--target", "-t", default="twi", help="Target language code")
    translate_parser.add_argument("--source", "-s", default="en", help="Source language code")
    translate_parser.add_argument("--terminology", "-tm", help="Path to terminology CSV file")
    translate_parser.add_argument("--output", "-o", choices=["text", "json"], default="text", 
                                help="Output format")
    
    # List terminology command
    list_parser = subparsers.add_parser("list", help="List available terminology")
    list_parser.add_argument("--terminology", "-tm", help="Path to terminology CSV file")
    
    # Export terminology command
    export_parser = subparsers.add_parser("export", help="Export terminology")
    export_parser.add_argument("--terminology", "-tm", required=True, help="Path to terminology CSV file")
    export_parser.add_argument("--format", "-f", choices=["json", "csv"], default="json", 
                              help="Output format")
    
    # Create sample command
    sample_parser = subparsers.add_parser("sample", help="Create sample terminology")
    sample_parser.add_argument("--output", "-o", default="sample_terminology.csv", 
                              help="Output file path")
    
    args = parser.parse_args()
    
    if args.command == "translate":
        translator = NkraneTranslator(
            target_lang=args.target,
            src_lang=args.source,
            terminology_source=args.terminology
        )
        
        result = translator.translate(args.text)
        
        if args.output == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result['text'])
    
    elif args.command == "list":
        options = list_available_options(args.terminology)
        print(json.dumps(options, indent=2))
    
    elif args.command == "export":
        output = export_terminology(args.terminology, args.format)
        print(output)
    
    elif args.command == "sample":
        save_sample_terminology(args.output)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
