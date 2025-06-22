import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

from src.config import settings

logger = logging.getLogger(__name__)

class GoogleSheetService:
    """Service for interacting with Google Sheets."""
    def __init__(self):
        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.creds = None
        self.client = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Sheets API."""
        try:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                settings.GOOGLE_CREDENTIALS_PATH, self.scope
            )
            self.client = gspread.authorize(self.creds)
            logger.info("Успешная аутентификация с Google Sheets API.")
        except FileNotFoundError:
            logger.error(f"Файл с учетными данными не найден: {settings.GOOGLE_CREDENTIALS_PATH}")
        except Exception as e:
            logger.error(f"Ошибка аутентификации с Google Sheets API: {e}")

    def get_employees(self) -> list[dict] | None:
        """Fetches all records from the Employees sheet."""
        if not self.client:
            logger.error("Клиент Google Sheets не инициализирован.")
            return None
        try:
            sheet = self.client.open_by_key(settings.EMPLOYEES_SHEET_ID).worksheet("Employees")
            records = sheet.get_all_records()
            logger.info(f"Загружено {len(records)} записей сотрудников.")
            return records
        except gspread.exceptions.SpreadsheetNotFound:
            logger.error(f"Таблица с ID {settings.EMPLOYEES_SHEET_ID} не найдена.")
            return None
        except gspread.exceptions.WorksheetNotFound:
            logger.error("Лист 'Employees' не найден в таблице.")
            return None
        except Exception as e:
            logger.error(f"Ошибка при чтении данных из Google Sheets: {e}")
            return None

# Синглтон-экземпляр сервиса
google_sheets_service = GoogleSheetService()
