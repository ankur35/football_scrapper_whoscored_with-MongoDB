
class Cleaner(object):

    def clean_spaces(self, item):
        return item.strip()

    def clean_dash(self, item):
        if item == '-':
            return None
        return item

    def clean_percent_sign(self, item):
        if item.endswith('%'):
            return item[:-1]
        return item


class TeamDataCleaner(Cleaner):

    def clean(self, data):
        clean_data = {}

        for section_name, section in data.items():
            if not section_name == 'profile_data':
                clean_section = []

                for row in section:
                    clean_row = {}

                    for k, v in row.items():
                        v = self.clean_spaces(v)
                        v = self.clean_percent_sign(v)
                        v = self.clean_dash(v)
                        clean_row[k] = v
 
                    clean_section.append(clean_row)
            else:
                clean_section = {}

                for k, v in section.items():
                    v = self.clean_spaces(v)
                    v = self.clean_percent_sign(v)
                    v = self.clean_dash(v)
                    clean_section[k] = v

            clean_data[section_name] = clean_section
        return clean_data



class MatchReportCleaner(Cleaner):

    def clean(self, data):
        clean_data = {}

        for k, v in data.items():
            clean_values = []

            for vv in v:
                clean_value = self.clean_spaces(vv)
                clean_value = self.clean_dash(clean_value)
                clean_value = self.clean_percent_sign(clean_value)
                clean_values.append(clean_value)
            
            clean_data[k] = clean_values
        
        return clean_data