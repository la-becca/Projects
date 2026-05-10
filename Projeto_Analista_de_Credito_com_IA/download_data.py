from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


COMPETITION = "home-credit-default-risk"
ZIP_NAME = f"{COMPETITION}.zip"
REQUIRED_FILES = [
    "application_train.csv",
    "application_test.csv",
    "bureau.csv",
    "bureau_balance.csv",
    "credit_card_balance.csv",
    "installments_payments.csv",
    "POS_CASH_balance.csv",
    "previous_application.csv",
    "sample_submission.csv",
    "HomeCredit_columns_description.csv",
]


def find_kaggle_command() -> str:
    kaggle = shutil.which("kaggle")
    if kaggle:
        return kaggle

    scripts_dir = Path(sys.executable).resolve().parent / "Scripts"
    kaggle_exe = scripts_dir / ("kaggle.exe" if sys.platform == "win32" else "kaggle")
    if kaggle_exe.exists():
        return str(kaggle_exe)

    raise SystemExit(
        "Kaggle CLI nao encontrado. Instale com: python -m pip install kaggle"
    )


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    missing_files = [name for name in REQUIRED_FILES if not (project_dir / name).exists()]

    if not missing_files:
        print("Base ja encontrada. Nada para baixar.")
        return

    kaggle = find_kaggle_command()
    zip_path = project_dir / ZIP_NAME

    if not zip_path.exists():
        print("Baixando base do Kaggle...")
        subprocess.run(
            [
                kaggle,
                "competitions",
                "download",
                "-c",
                COMPETITION,
                "-p",
                str(project_dir),
            ],
            check=True,
        )
    else:
        print(f"Arquivo {ZIP_NAME} ja existe. Pulando download.")

    print("Descompactando arquivos...")
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(project_dir)

    missing_after_extract = [
        name for name in REQUIRED_FILES if not (project_dir / name).exists()
    ]
    if missing_after_extract:
        raise SystemExit(
            "Download/descompactacao incompleta. Arquivos ausentes: "
            + ", ".join(missing_after_extract)
        )

    print("Base pronta para uso.")


if __name__ == "__main__":
    main()
