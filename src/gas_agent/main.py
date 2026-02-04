"""
CLI entrypoint: run HMIS table fill pipeline.
"""

import sys
from pathlib import Path

from gas_agent.pipeline import run_pipeline
from dotenv import load_dotenv

load_dotenv()

def main() -> None:
    """
    Simple CLI: 
    - Default: Fill entire table from docs/HMIS TABLE.xlsx → docs/HMIS_filled.xlsx
    - --dryrun: Process first 2 rows WITH LLM/search (for testing)
    """
    # Check for dry-run flag
    dry_run = "--dryrun" in sys.argv
    
    # Default paths
    input_path = Path("docs/HMIS TABLE.xlsx")
    output_path = Path("docs/HMIS_filled.xlsx")
    
    # Validate input exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        print("Please ensure docs/HMIS TABLE.xlsx exists")
        sys.exit(1)
    
    # Run pipeline
    if dry_run:
        print("🧪 DRY RUN MODE: Processing first 2 rows WITH LLM + web search")
        print("   (This is a real test of the full pipeline)")
        print()
        
        records = run_pipeline(
            input_path,
            output_path=output_path,
            max_rows=2,
        )
        print()
        print(f"✓ Dry run complete: {len(records)} rows filled and saved to {output_path}")
    else:
        print("🚀 FULL RUN: Processing all 197 rows with LLM + web search")
        print(f"   Input:  {input_path}")
        print(f"   Output: {output_path}")
        print("   (This will take ~4-5 hours for 197 rows)")
        print()
        
        records = run_pipeline(
            input_path,
            output_path=output_path,
        )
        print()
        print(f"✓ Complete: {len(records)} rows filled and saved to {output_path}")


if __name__ == "__main__":
    main()
