"use strict";
(function () {
  CKEDITOR.dialog.add("spotify", function (editor) {
    return {
      title: editor.lang.spotify.title,
      minWidth: 200,
      minHeight: 100,
      contents: [
        {
          id: "spotify",
          elements: [
            {
              id: "embedCode",
              type: "text",
              label: editor.lang.spotify.embedCodeLabel,
              width: "200px",
              setup: function (widget) {
                this.setValue(widget.data.embedCode);
              },
              commit: function (widget) {
                widget.setData("embedCode", this.getValue());
              },
              validate: validateEmbedCode(editor.lang.spotify.embedCodeError),
            },
            {
              id: "align",
              type: "select",
              label: editor.lang.common.align,
              items: [
                [editor.lang.common.notSet, ""],
                [editor.lang.common.alignLeft, "left"],
                [editor.lang.common.alignRight, "right"],
                [editor.lang.common.alignCenter, "center"],
              ],
              setup: function (widget) {
                this.setValue(widget.data.align);
              },
              commit: function (widget) {
                widget.setData("align", this.getValue());
              },
            },
            {
              type: "hbox",
              widths: ["50%", "50%"],
              children: [
                {
                  id: "width",
                  type: "text",
                  label: editor.lang.common.width,
                  width: "100px",
                  setup: function (widget) {
                    this.setValue(widget.data.width);
                  },
                  commit: function (widget) {
                    widget.setData("width", this.getValue());
                  },
                },
                {
                  id: "height",
                  type: "text",
                  label: editor.lang.common.height,
                  width: "100px",
                  setup: function (widget) {
                    this.setValue(widget.data.height);
                  },
                  commit: function (widget) {
                    widget.setData("height", this.getValue());
                  },
                },
              ],
            },
          ],
        },
      ],
    };
  });

  function validateEmbedCode(errorMsg) {
    // spotify:track:6rqhFgbbKwnb9MLmUQDhG6
    var spotifyURIRegex =
      /^spotify:(album|playlist|track|artist):([a-zA-Z0-9]{22})$/;
    // https://open.spotify.com/album/4RuzGKLG99XctuBMBkFFOC
    var spotifyURLRegex =
      /^https?:\/\/open\.spotify\.com\/(album|playlist|track|artist)\/([a-zA-Z0-9]{22})(\?si\=[a-z0-9]{16})?$/;

    return function () {
      var embedCode = this.getValue();

      return (
        spotifyURIRegex.test(embedCode) ||
        spotifyURLRegex.test(embedCode) ||
        errorMsg
      );
    };
  }
})();
