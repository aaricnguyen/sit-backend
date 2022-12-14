import Bluebird from 'bluebird';
import { parseInsightInput } from '../components/Insight/InputHandler';
// import InsightTemplate from '../components/Insight/InsightTemplate';
// import InsightTemplate from '../components/Insight/insightTemplate.json';
import { responseSuccess } from '../services/Response';
import ManageInsightAPIs from '../components/Insight/ManageInsightAPIs';
import fs from 'fs';
export const getAll = async (req, res) => {
  const InsightTemplate = fs.readFileSync(
    './src/components/Insight/insightTemplate.json',
    { encoding: 'utf8', flag: 'r' },
  );
  const data = await Bluebird.map(
    JSON.parse(InsightTemplate),
    async (insight) => {
      const { key = '', template = '' } = insight;

      const inputParsed = await parseInsightInput(key);

      const { type = '', data } = inputParsed;
      const resultValue = await ManageInsightAPIs(type, data);
      const resultTemplate = template.replace(/%/g, `${resultValue.result}%`);

      return {
        key,
        template,
        resultTemplate,
        resultValue,
      };
    },
  );

  res.json(
    responseSuccess({
      data,
    }),
  );
};

export const uploadTemplateFile = async (req, res) => {
  const InsightTemplate = fs.readFileSync(
    `./src/components/Insight/template.json`,
    { encoding: 'utf8' },
  );

  return res.json(
    responseSuccess({
      data: InsightTemplate,
    }),
  );
};

export const updatedTemplateFile = async (req, res) => {
  try {
    fs.readFile(
      './src/components/Insight/template.json',
      'utf8',
      function (err, data) {
        if (err) {
          return console.log(err);
        }

        fs.writeFile(
          './src/components/Insight/insightTemplate.json',
          data,
          'utf8',
          function (err) {
            if (err) return console.log(err);
          },
        );
      },
    );
    return res.json(
      responseSuccess({
        message: 'updated successfuly!',
      }),
    );
  } catch (error) {
    return res.json(
      responseSuccess({
        message: error,
      }),
    );
  }
};
