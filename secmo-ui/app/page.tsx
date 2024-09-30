"use client";

import { Input } from "@nextui-org/input";
import { useEffect, useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
} from "@nextui-org/react";

import { EmailIcon } from "@/components/icons";

export default function Home() {
  const [logs, setLogs] = useState("");
  const [report, setReport] = useState(""); // New state for report
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  // Load logs and report from localStorage
  useEffect(() => {
    const savedLogs = localStorage.getItem("logs");
    const savedReport = localStorage.getItem("report"); // Load previous report

    if (savedLogs) {
      setLogs(savedLogs);
    }

    if (savedReport) {
      setReport(savedReport);
    }
  }, []);

  // Fetch logs and save them to localStorage
  const fetchLogs = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_ENDPOINT}/logs`);
      const data = await response.text();

      setLogs(data);
      localStorage.setItem("logs", data);
    } catch (error) {}
  };

  // Trigger report generation and fetch logs
  const handleTrigger = async () => {
    setLoading(true);
    await fetchLogs(); // Fetch logs when the button is clicked
    await triggerReport(); // Then trigger the report

    setLoading(false);
  };

  // Trigger report generation and store the report in HTML format
  const triggerReport = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_ENDPOINT}/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        },
      );

      const reportHTML = await response.text();

      setReport(reportHTML);
      localStorage.setItem("report", reportHTML);

      if (email) {
        onOpen();
      } else {
        onOpen();
      }
    } catch (error) {}
  };

  const emailInput = (
    <Input
      aria-label="Email"
      className="py-4 px-8  text-white  dark:text-black"
      labelPlacement="outside"
      placeholder="Send Report To (Optional)"
      startContent={
        <EmailIcon className="text-base text-default-400 pointer-events-none flex-shrink-0" />
      }
      type="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
    />
  );

  return (
    <section className="min-h-screen dark:bg-black bg-gray-50 flex flex-col items-center py-12">
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                Report Generated
              </ModalHeader>
              <ModalBody>
                <p>Check Submitted Email for Report Analysis</p>
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>

      {/* Header */}
      <div className="text-center max-w-2xl mx-auto mb-10">
        <h1
          className={
            "text-4xl font-extrabold leading-tight dark:text-gray-200 text-gray-800"
          }
        >
          Log Monitoring Dashboard
        </h1>
        <p className={"text-lg dark:text-gray-500 text-gray-500 mt-4"}>
          Seamlessly monitor logs and generate detailed reports with ease.
        </p>
      </div>

      {/* Logs and Report Section */}
      <div className="max-w-5xl w-full px-6 md:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Logs Card */}
          <div className="bg-white dark:bg-gray-900 shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-semibold dark:text-gray-200 text-gray-700 mb-4">
              Logs
            </h2>
            <div className="dark:bg-gray-700 bg-gray-100 p-4 rounded-lg dark:text-white h-64 overflow-auto">
              <div dangerouslySetInnerHTML={{ __html: logs }} />
            </div>
          </div>

          {/* Report Card */}
          <div className="bg-white dark:bg-gray-900 shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-semibold dark:text-gray-200 text-gray-700 mb-4">
              Report
            </h2>
            <div className="dark:bg-gray-700 bg-gray-100 p-4 rounded-lg dark:text-white h-64 overflow-auto">
              <div dangerouslySetInnerHTML={{ __html: report }} />
            </div>
          </div>
        </div>
      </div>

      {/* Email Input and Trigger Report */}
      <div className="mt-8 max-w-2xl w-full px-6 md:px-8">
        <div className="flex flex-col md:flex-row items-center gap-4">
          {emailInput}

          <Button
            className={`py-4 px-8 bg-black text-white dark:text-black dark:bg-white shadow-sm`}
            isLoading={loading}
            onClick={handleTrigger}
          >
            Generate Report
          </Button>
        </div>
      </div>
    </section>
  );
}
