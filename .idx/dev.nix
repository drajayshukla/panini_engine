{ pkgs, ... }: {
  # Configuration for the Pāṇinian Engine Environment
  channel = "stable-24.05"; 

  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
  ];

  idx = {
    # Extensions for Aṣṭādhyāyī logic development
    extensions = [
      "ms-python.python"
      "ms-python.vscode-pylance"
    ];

    # Configure the Streamlit Web Preview
    previews = {
      enable = true;
      previews = {
        web = {
          # Use bash to activate venv and run the Pāṇini app
          command = ["bash" "-c" "source .venv/bin/activate && streamlit run app.py --server.port $PORT --server.address 0.0.0.0"];
          manager = "web";
          env = {
            PORT = "$PORT";
          };
        };
      };
    };

    # Lifecycle hooks to automate your setup
    workspace = {
      onCreate = {
        # This builds your Sanskrit lab automatically
        setup-venv = "python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt";
      };
    };
  };
}